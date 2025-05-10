document.addEventListener('DOMContentLoaded', function() {
  const form = document.querySelector('form');
  
  if (form) {
    form.addEventListener('submit', function(event) {
      event.preventDefault();

      // Limpia mensajes de error previos
      document.getElementById("nameError").textContent = "";
      document.getElementById("apellidoError") ? document.getElementById("apellidoError").textContent = "" : null;
      document.getElementById("emailError").textContent = "";
      document.getElementById("passwordError").textContent = "";

      // Obtenemos los datos del formulario
      const name = document.getElementById("name").value.trim();
      const lastname = document.getElementById("lastname").value.trim();
      const email = document.getElementById("email").value.trim();
      const password = document.getElementById("password").value.trim();

      // expresiones regulares para validaciones
      const nameRegex = /^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$/;
      const emailRegex = /^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$/i;
      const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$/;

      let valid = true;
      let errorMessages = [];

      // Validar nombre
      if (!name) {
        document.getElementById("nameError").textContent = "El nombre es obligatorio.";
        errorMessages.push("El nombre es obligatorio.");
        valid = false;
      } else if (!nameRegex.test(name)) {
        document.getElementById("nameError").textContent = "El nombre solo puede contener letras.";
        errorMessages.push("El nombre solo puede contener letras.");
        valid = false;
      }

      // Validar apellido
      if (!lastname) {
        document.getElementById("apellidoError").textContent = "El apellido es obligatorio.";
        errorMessages.push("El apellido es obligatorio.");
        valid = false;
      } else if (!nameRegex.test(lastname)) {
        document.getElementById("apellidoError").textContent = "El apellido solo puede contener letras.";
        errorMessages.push("El apellido solo puede contener letras.");
        valid = false;
      }

      // Validar email
      if (!email) {
        document.getElementById("emailError").textContent = "El correo es obligatorio.";
        errorMessages.push("El correo es obligatorio.");
        valid = false;
      } else if (!emailRegex.test(email)) {
        document.getElementById("emailError").textContent = "Ingrese un correo válido.";
        errorMessages.push("Ingrese un correo válido.");
        valid = false;
      }

      // Validar contraseña
      if (!password) {
        document.getElementById("passwordError").textContent = "La contraseña es obligatoria.";
        errorMessages.push("La contraseña es obligatoria.");
        valid = false;
      } else if (!passwordRegex.test(password)) {
        document.getElementById("passwordError").textContent = "Debe tener al menos 6 caracteres, una letra y un número.";
        errorMessages.push("La contraseña debe tener al menos 6 caracteres, una letra y un número.");
        valid = false;
      }

      // Si hay errores, se muestra con SweetAlert
      if (!valid) {
        Swal.fire({
          icon: 'error',
          title: 'Error de validación',
          html: errorMessages.map(msg => `• ${msg}`).join('<br>'),
          confirmButtonColor: '#6d4c41'
        });
        return;
      }

      // Si todo esta correcto, envia el formulario
      Swal.fire({
        icon: 'success',
        title: '¡Registro exitoso!',
        text: 'Tu cuenta ha sido creada correctamente.',
        confirmButtonColor: '#6d4c41',
        timer: 2000,
        timerProgressBar: true
      }).then(() => {
        form.submit();
      });
    });
  } else {
    console.error('No se encontró el formulario en el documento');
  }
});