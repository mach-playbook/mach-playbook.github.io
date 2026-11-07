# Prevención de Bloqueos Desatendidos, Timeouts y Estándar de Ejecución Continua (Zero-Hang Protocol)

> [!IMPORTANT]
> **REGLA DE ORO DE AUTOMATIZACIÓN DESATENDIDA PARA MACH-PLAYBOOK:**
> Queda terminantemente PROHIBIDO lanzar tareas en segundo plano que puedan requerir interacción de teclado, solicitud de contraseñas (`sudo`), confirmaciones interactivas (`[y/N]`) o que carezcan de un límite estricto de tiempo (*timeout*). Todo script, comando del agente en WSL o paso de GitHub Actions debe ser 100% autónomo, inmune a bloqueos en `stdin`, contar con timeouts de red/socket y tener salvaguardas de salida limpia.

---

## 1. Contexto y Análisis de Vulnerabilidades en `mach-playbook`

En entornos con flujos de trabajo autónomos como `mach-playbook` (publicación diaria automática con Gemini AI, pruebas unitarias de compilación con Docker/HTML-Proofer, inspecciones con Chrome DevTools Protocol y sindicación en redes), existen puntos críticos donde un proceso sin supervisión humana puede congelarse indefinidamente:

1. **Solicitud de `sudo` en WSL / terminal:** Cuando expira la sesión de superusuario, cualquier invocación de `sudo` bloquea la entrada estándar (`stdin`) esperando una clave. En una sesión desatendida del agente, el proceso se congela consumiendo 0% de CPU y el agente entra en espera pasiva infinita.
2. **Petición interactiva de credenciales Git:** Si un `git pull --rebase` o `git push` encuentra un conflicto o desajuste de token sin `GIT_TERMINAL_PROMPT=0`, Git queda a la espera de credenciales interactivas en la consola.
3. **Peticiones HTTP sin Timeout:** Llamadas de red mediante `requests`, `urllib.request` o `fetch` sin parámetro de timeout quedan colgadas en espera de respuesta de socket si el servidor remoto (Dev.to, Buffer, Unsplash, Google API) experimenta latencia o desconexión.
4. **Flujos de GitHub Actions sin `timeout-minutes`:** Por defecto, GitHub Actions espera hasta 360 minutos (6 horas) antes de cancelar un job colgado, agotando minutos de runner y reteniendo bloqueos de concurrencia.
5. **Navegadores Headless (Chrome / CDP) Zombis:** Si una instancia de Chromium iniciada mediante subproceso no recibe respuesta o falla antes de ejecutar `kill()`, permanece como proceso zombi bloqueando puertos de depuración.

---

## 2. Los 5 Principios Inmutables del Protocolo "Zero-Hang"

Para blindar el repositorio contra cualquier bloqueo desatendido, todo agente de IA, automatización o desarrollador debe aplicar estrictamente los siguientes 5 principios:

### Principio 1: Prohibición Absoluta de `sudo` en Scripts y Comandos del Agente
* **Regla:** NUNCA utilizar `sudo` en comandos ejecutados por herramientas de IA, scripts en `scripts/` o pasos de integración continua.
* **Alternativa Canónica para Docker:** Si se requiere manipular archivos o ejecutar comandos con privilegios elevados en contenedores, se DEBE usar el usuario `root` (`-u 0` o `--user 0`) dentro del propio contenedor:
  ```bash
  # CORRECTO: Ejecuta como root dentro del contenedor sin pedir contraseña en el host
  docker exec -u 0 mach-playbook-site chmod 644 /usr/share/nginx/html/index.html

  # PROHIBIDO: Solicita password interactivo en WSL y congela la sesión desatendida
  sudo chmod -R 777 _site/
  ```

### Principio 2: Timeouts Defensivos Obligatorios en Comandos y GitHub Actions
* **Regla en CLI / Shell:** Ningún comando de larga duración (Docker build, compilación Jekyll, tests E2E) debe lanzarse sin envolverse en la utilidad `timeout` de GNU coreutils:
  ```bash
  # El comando aborta forzosamente tras 300 segundos liberando al agente
  timeout 300s docker build --target test -t mach-playbook:test .
  timeout 180s bundle exec jekyll build
  timeout 60s python3 scripts/test-adsense-compliance.py
  ```
* **Regla en GitHub Actions:** Todo job o paso susceptible de demorarse DEBE definir `timeout-minutes`:
  ```yaml
  jobs:
    publish-daily-post:
      runs-on: ubuntu-latest
      timeout-minutes: 15
  ```

### Principio 3: Desacople de Entrada Estándar (`< /dev/null`) y Modo No-Interactivo
* **Regla:** Todo proceso desatendido debe cerrar su canal de entrada estándar o definir banderas explícitas para abortar de inmediato con error ante cualquier intento de solicitud interactiva:
  ```bash
  # Si un script solicita input inesperado, fallará al instante en vez de colgarse
  python3 scripts/publish_daily_jekyll_post.py < /dev/null
  ```
* **Banderas Requeridas en el Repositorio:**
  * **Git:** Configurar siempre `GIT_TERMINAL_PROMPT=0` y `-c core.askPass=true` para no esperar credenciales en terminal.
  * **APT / Sistema:** `DEBIAN_FRONTEND=noninteractive`.
  * **NPM / Pip:** `npm install --no-audit --no-fund --yes`, `pip install --no-input`.

### Principio 4: Timeouts Obligatorios en Sockets y Peticiones HTTP
* **Regla:** Queda prohibida cualquier llamada HTTP sin timeout explícito.
* **Python (`requests` y `urllib.request`):**
  ```python
  # CORRECTO: Timeout estricto de socket (10 a 20 segundos)
  response = requests.post(DEVTO_API_URL, json=payload, headers=headers, timeout=15)
  with urllib.request.urlopen(req, timeout=12) as response:
      data = response.read()

  # PROHIBIDO: Se cuelga indefinidamente si la conexión cae a nivel TCP
  response = requests.post(DEVTO_API_URL, json=payload, headers=headers)
  req = urllib.request.urlopen(url)
  ```
* **Node.js (`fetch` / AbortController):**
  ```javascript
  // CORRECTO: AbortController cancela la solicitud tras 4 segundos
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 4000);
  const response = await fetch(url, { signal: controller.signal });
  clearTimeout(timeoutId);
  ```

### Principio 5: Heartbeat Watchdog, Checkpoints en Disco y Circuit Breakers
* **Regla de Checkpoints:** Para tareas por lotes de larga duración (reescritura masiva de artículos, conversión de imágenes, sindicación histórica), los scripts deben almacenar su estado en archivos JSON de progreso (`.progress.json` o `.devto_synced.json`):
  * Guardar offset actual, marcas de tiempo, número de procesados y errores.
  * Si el proceso es interrumpido o reiniciado, retoma desde el último offset guardado en disco sin duplicar operaciones.
* **Regla de Circuit Breakers y Fallbacks:** Si un servicio externo falla (por ejemplo, cuota 429 de Gemini o caída de CDN de imágenes):
  * El script no debe colgarse ni abortar el pipeline principal de forma descontrolada.
  * Debe aplicar retroceso exponencial (*exponential backoff*) y activar fallbacks algorítmicos autónomos (como la síntesis local tridimensional en `publish_daily_jekyll_post.py` o placeholders de imágenes locales).

---

## 3. Matriz de Prevención de Fallos en `mach-playbook`

| Escenario de Riesgo | Síntoma / Error | Medida Preventiva Inmediata |
|---|---|---|
| **Permisos de archivos creados por Docker** | `Permission denied` en el host WSL al editar `_site/` | Ejecutar `docker exec -u 0 <container> chmod ...` |
| **Petición interactiva de credenciales Git** | Proceso congelado en `Username for 'https://github.com':` | Definir variable de entorno `GIT_TERMINAL_PROMPT=0` |
| **API de terceros lenta o no disponible** | Script `publish_to_devto.py` o `publish_to_buffer.py` congelado | Parámetro `timeout=15` en `requests.post` |
| **Caída de CDN en generación de imágenes** | `generate-images.js` bloqueado en Unsplash | `AbortController` con timeout de 4000 ms en llamada `fetch` |
| **Procesos Chrome CDP colgados** | Puertos 9455/9456 bloqueados tras fallo en tests | Bloque `try...finally` garantizando `chrome.kill()` y `timeout=10` en `urlopen` |
| **Paso de GitHub Actions trabado** | Runner consumiendo cuota hasta el límite de 6 horas | Declarar `timeout-minutes: 15` a nivel de job en todos los workflows |
| **Llamada interactiva en scripts del agente** | Agente en espera infinita aguardando respuesta de terminal | Ejecutar comandos desatendidos con `< /dev/null` |

---

## 4. Protocolo Operativo para el Agente en Ausencia del Usuario

Cuando el usuario asigne tareas de larga duración o ejecuciones en segundo plano (vía comandos como `/goal`, tareas programadas o ejecución nocturna), el agente DEBE:

1. **Pre-Flight Check de Inmunidad:**
   - Verificar que ningún comando a despachar contenga `sudo`.
   - Verificar que los scripts tengan timeouts configurados en todos sus sockets.
   - Declarar límites de tiempo con `timeout <Ns>` en llamadas de shell complejas.
2. **Desacoplar la entrada interactiva:** Añadir siempre `< /dev/null` a comandos de shell que no requieran explícitamente interacción.
3. **Supervisión de salida en tiempo real:** Redirigir salidas a logs rotacionales o verificar los códigos de salida de los comandos en vez de confiar en esperas pasivas.
4. **Recuperación Automática ante Fallo:** Si un subproceso es terminado por `timeout` (código de salida 124), el agente debe interpretar el fallo como un cuello de botella, registrar el incidente y continuar con la siguiente tarea de la lista sin quedar bloqueado.

