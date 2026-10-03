---
title: Contact
icon: fas fa-envelope
order: 7
---

<div class="lang-block lang-es" markdown="1">

# Contacto & Asesoría Técnica

¿Tienes una duda de arquitectura, retroalimentación técnica o requieres consultoría para tu transición a arquitecturas MACH o Composable Commerce? Estamos siempre disponibles para dialogar con otros ingenieros de software, líderes técnicos y arquitectos de soluciones.

## Canales Directos

* **Email:** [merolhack@gmail.com](mailto:merolhack@gmail.com)
* **Autor:** Lenin Meza (Senior Solutions Architect & Full-Stack Engineer)
* **Portafolio:** [merolhack.github.io](https://merolhack.github.io/)
* **LinkedIn:** [linkedin.com/in/leninmezazarco](https://www.linkedin.com/in/leninmezazarco)
* **GitHub:** [github.com/merolhack](https://github.com/merolhack)

---

## Formulario de Mensaje Directo

<form action="https://formspree.io/f/xoevgrqq" method="POST" class="contact-form">
  <input type="text" name="_gotcha" style="display:none">
  <div class="mb-3">
    <label for="name-es" class="form-label font-weight-bold">Nombre Completo</label>
    <input type="text" class="form-control" id="name-es" name="name" required placeholder="Tu Nombre">
  </div>
  <div class="mb-3">
    <label for="email-es" class="form-label font-weight-bold">Correo Electrónico</label>
    <input type="email" class="form-control" id="email-es" name="_replyto" required placeholder="tu-email@empresa.com">
  </div>
  <div class="mb-3">
    <label for="subject-es" class="form-label font-weight-bold">Asunto</label>
    <input type="text" class="form-control" id="subject-es" name="_subject" required placeholder="Consulta de Arquitectura / Feedback Técnico">
  </div>
  <div class="mb-3">
    <label for="message-es" class="form-label font-weight-bold">Mensaje o Escenario Técnico</label>
    <textarea class="form-control" id="message-es" name="message" rows="5" required placeholder="Describe tu consulta o desafío de arquitectura..."></textarea>
  </div>
  <button type="submit" class="btn btn-primary px-4 py-2">Enviar Mensaje</button>
</form>

---

## Tiempo de Respuesta

Revisamos consultas con regularidad y respondemos en un plazo de 24 a 48 horas hábiles. Para reportes de bugs o mejoras al código abierto, también puedes abrir un Issue o Pull Request en nuestro [repositorio de GitHub](https://github.com/merolhack/mach-playbook).

</div>

<div class="lang-block lang-en d-none" markdown="1">

# Contact & Enterprise Advisory

Have an architectural question, technical feedback, or an inquiry regarding enterprise consulting? We welcome discussions with fellow solutions architects, software engineers, and technology leaders.

## Direct Inquiries

* **Email:** [merolhack@gmail.com](mailto:merolhack@gmail.com)
* **Author:** Lenin Meza (Senior Solutions Architect & Lead Engineer)
* **Professional Portfolio:** [merolhack.github.io](https://merolhack.github.io/)
* **LinkedIn:** [linkedin.com/in/leninmezazarco](https://www.linkedin.com/in/leninmezazarco)
* **GitHub:** [github.com/merolhack](https://github.com/merolhack)

---

## Send a Message

<form action="https://formspree.io/f/xoevgrqq" method="POST" class="contact-form">
  <input type="text" name="_gotcha" style="display:none">
  <div class="mb-3">
    <label for="name-en" class="form-label font-weight-bold">Your Name</label>
    <input type="text" class="form-control" id="name-en" name="name" required placeholder="Jane Doe">
  </div>
  <div class="mb-3">
    <label for="email-en" class="form-label font-weight-bold">Your Email</label>
    <input type="email" class="form-control" id="email-en" name="_replyto" required placeholder="jane@example.com">
  </div>
  <div class="mb-3">
    <label for="subject-en" class="form-label font-weight-bold">Subject</label>
    <input type="text" class="form-control" id="subject-en" name="_subject" required placeholder="Architecture Consultation / Technical Feedback">
  </div>
  <div class="mb-3">
    <label for="message-en" class="form-label font-weight-bold">Message</label>
    <textarea class="form-control" id="message-en" name="message" rows="5" required placeholder="Detail your question or enterprise scenario..."></textarea>
  </div>
  <button type="submit" class="btn btn-primary px-4 py-2">Send Message</button>
</form>

---

## Response Time & Advisory Scope

We review technical inquiries regularly and aim to respond within 24–48 business hours. For bug reports or repository contributions, feel free to open an issue or pull request directly on our [GitHub repository](https://github.com/merolhack/mach-playbook).

</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  const forms = document.querySelectorAll(".contact-form");
  forms.forEach(function (form) {
    form.addEventListener("submit", async function (e) {
      e.preventDefault();
      const btn = form.querySelector('button[type="submit"]');
      const originalText = btn.innerHTML;
      btn.disabled = true;
      btn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Enviando... / Sending...';

      let statusMsg = form.querySelector(".form-status-alert");
      if (!statusMsg) {
        statusMsg = document.createElement("div");
        statusMsg.className = "form-status-alert mt-3 alert d-none";
        form.appendChild(statusMsg);
      }

      try {
        const formData = new FormData(form);
        const response = await fetch(form.action, {
          method: form.method,
          body: formData,
          headers: { "Accept": "application/json" }
        });
        if (response.ok) {
          form.reset();
          statusMsg.className = "form-status-alert mt-3 alert alert-success";
          statusMsg.innerHTML = '<i class="fas fa-check-circle me-2"></i>¡Mensaje enviado con éxito! Te responderemos a la brevedad. / Message sent successfully!';
        } else {
          const data = await response.json();
          statusMsg.className = "form-status-alert mt-3 alert alert-danger";
          statusMsg.innerHTML = '<i class="fas fa-exclamation-circle me-2"></i>' + (data.errors ? data.errors.map(err => err.message).join(", ") : "Error al enviar el mensaje. / Submission error.");
        }
      } catch (err) {
        statusMsg.className = "form-status-alert mt-3 alert alert-danger";
        statusMsg.innerHTML = '<i class="fas fa-exclamation-circle me-2"></i>Error de conexión. Inténtalo de nuevo. / Connection error.';
      } finally {
        btn.innerHTML = originalText;
        btn.disabled = false;
      }
    });
  });
});
</script>
