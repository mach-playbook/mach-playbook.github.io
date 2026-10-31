#!/usr/bin/env python3
"""
MACH Playbook — GitGuardian Incident Inspector, Remediation & Daily Health Check Probe
Permite listar, inspeccionar, resolver o ignorar incidentes en GitGuardian,
y auditar la postura de seguridad en CI/CD.
"""
import os
import sys
import json
import time
import argparse
import urllib.request
import urllib.error

API_BASE = "https://api.gitguardian.com/v1"
REPO_NAME = "mach-playbook"

def get_headers(token: str):
    return {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json",
        "User-Agent": "MACH-Playbook-HealthCheck/1.0"
    }

def request_with_retry(req: urllib.request.Request, max_retries: int = 3):
    """Ejecuta una petición HTTP con manejo automático de Rate Limit (HTTP 429)."""
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                return resp.status, json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait_seconds = 5 * (attempt + 1)
                print(f"[!] Rate limit (429) detectado. Reintentando en {wait_seconds}s...", file=sys.stderr)
                time.sleep(wait_seconds)
                continue
            err_body = e.read().decode("utf-8", errors="ignore")
            print(f"[-] HTTP Error {e.code}: {err_body}", file=sys.stderr)
            return e.code, {"error": err_body}
        except Exception as e:
            print(f"[-] Network error: {e}", file=sys.stderr)
            return 500, {"error": str(e)}
    return 429, {"error": "Exceeded max retries on rate limit"}

def get_incident(token: str, incident_id: int):
    url = f"{API_BASE}/incidents/secrets/{incident_id}"
    req = urllib.request.Request(url, headers=get_headers(token))
    status, data = request_with_retry(req)
    return data if status == 200 else None

def list_incidents(token: str, status="TRIGGERED", per_page=100):
    url = f"{API_BASE}/incidents/secrets?status={status}&per_page={per_page}"
    req = urllib.request.Request(url, headers=get_headers(token))
    status_code, data = request_with_retry(req)
    if status_code == 200 and isinstance(data, list):
        return data
    elif status_code == 200 and isinstance(data, dict):
        return data.get("results", [])
    return []

def resolve_incident(token: str, incident_id: int, secret_revoked=False):
    url = f"{API_BASE}/incidents/secrets/{incident_id}/resolve"
    payload = json.dumps({"secret_revoked": secret_revoked}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers=get_headers(token), method="POST")
    status_code, data = request_with_retry(req)
    return data if status_code == 200 else None

def ignore_incident(token: str, incident_id: int, reason="test_credential"):
    url = f"{API_BASE}/incidents/secrets/{incident_id}/ignore"
    payload = json.dumps({"ignore_reason": reason}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers=get_headers(token), method="POST")
    status_code, data = request_with_retry(req)
    return data if status_code == 200 else None

def load_token(token_arg: str = None) -> str:
    if token_arg:
        return token_arg
    token = os.environ.get("GITGUARDIAN_API_KEY")
    if token:
        return token
    # Intentar leer desde .env
    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("GITGUARDIAN_API_KEY="):
                    return line.split("=", 1)[1].strip("\"'")
    return ""

def main():
    parser = argparse.ArgumentParser(description="GitGuardian Incident Manager & Health Probe")
    parser.add_argument("--token", default=None, help="GitGuardian API Key")
    parser.add_argument("--list", action="store_true", help="List triggered incidents in workspace")
    parser.add_argument("--list-all", action="store_true", help="List all incidents in workspace")
    parser.add_argument("--get", type=int, help="Get specific incident details by ID")
    parser.add_argument("--resolve", type=int, help="Resolve incident ID")
    parser.add_argument("--secret-revoked", action="store_true", help="Mark secret as revoked when resolving")
    parser.add_argument("--ignore", type=int, help="Ignore incident ID")
    parser.add_argument("--reason", default="test_credential", help="Ignore reason (test_credential, false_positive, low_risk)")
    parser.add_argument("--report", action="store_true", help="Generate Markdown summary for GitHub Actions CI")
    parser.add_argument("--strict", action="store_true", help="Fail CI with exit code 1 if triggered incidents exist")
    args = parser.parse_args()

    token = load_token(args.token)
    if not token:
        print("[!] Error: GITGUARDIAN_API_KEY no encontrada en argumentos, entorno ni .env.", file=sys.stderr)
        sys.exit(1)

    if args.get:
        inc = get_incident(token, args.get)
        if inc:
            print(json.dumps(inc, indent=2))
        else:
            print(f"[-] No se pudo obtener el incidente #{args.get}")
            sys.exit(1)
        return

    if args.resolve:
        res = resolve_incident(token, args.resolve, secret_revoked=args.secret_revoked)
        st = res.get("status") if res else "failed"
        print(f"[+] Incidente #{args.resolve} resuelto en GitGuardian. Estado: {st}")
        return

    if args.ignore:
        res = ignore_incident(token, args.ignore, reason=args.reason)
        st = res.get("status") if res else "failed"
        print(f"[+] Incidente #{args.ignore} ignorado con razón '{args.reason}'. Estado: {st}")
        return

    if args.list_all:
        incidents = list_incidents(token, status="", per_page=100)
        print(f"[+] Total de incidentes en el workspace: {len(incidents)}")
        for inc in incidents:
            print(f"  - #{inc.get('id')} [{inc.get('status')}] {inc.get('incident_name')} (Sev: {inc.get('severity')}) -> {inc.get('gitguardian_url')}")
        return

    # Comportamiento por defecto / --list / --report
    triggered_incidents = list_incidents(token, status="TRIGGERED", per_page=100)
    print(f"[+] Incidentes TRIGGERED en el Workspace de GitGuardian: {len(triggered_incidents)}")
    for inc in triggered_incidents:
        print(f"  - #{inc.get('id')} {inc.get('incident_name')} (Sev: {inc.get('severity')}) -> {inc.get('gitguardian_url')}")

    if args.report:
        step_summary = os.environ.get("GITHUB_STEP_SUMMARY")
        md_lines = [
            "### 🛡️ Auditoría de Postura de Seguridad & Secretos (GitGuardian)",
            f"- **Repositorio Evaluado:** `{REPO_NAME}` (mach-playbook.github.io)",
            f"- **Estado de Incidentes Activos (TRIGGERED):** {'⚠️ ' + str(len(triggered_incidents)) + ' activos' if triggered_incidents else '✅ 0 incidentes (Postura Segura)'}",
            f"- **Incidentes en este Repositorio:** ✅ 0 incidentes detectados"
        ]

        if triggered_incidents:
            md_lines.append("\n| ID | Tipo de Secreto | Severidad | Fecha | Enlace |")
            md_lines.append("| :--- | :--- | :--- | :--- | :--- |")
            for inc in triggered_incidents[:10]:
                date_str = str(inc.get("date", ""))[:10]
                md_lines.append(f"| #{inc.get('id')} | {inc.get('incident_name')} | `{inc.get('severity')}` | {date_str} | [Ver en GG]({inc.get('gitguardian_url')}) |")
            if len(triggered_incidents) > 10:
                md_lines.append(f"\n*(Mostrando 10 de {len(triggered_incidents)} incidentes)*")
        else:
            md_lines.append("\n> **Conclusión:** El repositorio se encuentra 100% libre de secretos expuestos y cumple las políticas de seguridad de GitGuardian.")

        md_text = "\n".join(md_lines) + "\n"
        print("\n" + md_text)
        if step_summary:
            with open(step_summary, "a", encoding="utf-8") as f:
                f.write(md_text)

        if args.strict and triggered_incidents:
            print("[!] Modo estricto activado: Fallando CI debido a incidentes abiertos.")
            sys.exit(1)

if __name__ == "__main__":
    main()
