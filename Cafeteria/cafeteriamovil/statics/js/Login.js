document.addEventListener('DOMContentLoaded', function() {
  // Obtenemos el formulario
  const form = document.querySelector('form');
  
  // Verificamos que el formulario exista antes de añadir el event listener
  if (form) {
    form.addEventListener('submit', function(event) {
      event.preventDefault();

      // Limpiar mensajes de error previos
      document.getElementById("emailError").textContent = "";
      document.getElementById("passwordError").textContent = "";

      // Obtener datos del formulario
      const email = document.getElementById("email").value.trim();
      const password = document.getElementById("password").value.trim();

      // Definir expresiones regulares para validación
      const emailRegex = /^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$/i;
      const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$/;

      let valid = true;
      let errorMessages = [];

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
        document.getElementById("passwordError").textContent = "La contraseña debe tener al menos 6 caracteres, una letra y un número.";
        errorMessages.push("La contraseña debe tener al menos 6 caracteres, una letra y un número.");
        valid = false;
      }

      // Si hay errores, mostrar con SweetAlert
      if (!valid) {
        Swal.fire({
          icon: 'error',
          title: 'Error de validación',
          html: errorMessages.map(msg => `• ${msg}`).join('<br>'),
          confirmButtonColor: '#6d4c41'
        });
        return;
      }

      // Si todo esta correcto en las validaciones, procedemos a enviar
      const formData = new FormData(form);
      
      fetch(form.action, {
          method: 'POST',
          body: formData,
          headers: {
              'X-Requested-With': 'XMLHttpRequest'
          }
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          // Guardamos el token en localStorage
          if (data.token) {
            localStorage.setItem("token", data.token);
          }
          
          // Login exitoso
          Swal.fire({
            icon: 'success',
            title: '¡Inicio de sesión exitoso!',
            text: 'Redirigiendo...',
            confirmButtonColor: '#6d4c41',
            timer: 1500,
            timerProgressBar: true,
            showConfirmButton: false
          }).then(() => {
            // Redireccionamos al perfil
            window.location.href = '/usuario/';
          });
        } else {
          // En caso de error (usuario no encontrado o contraseña incorrecta)
          Swal.fire({
            icon: 'error',
            title: 'Error de autenticación',
            text: data.error || 'No se pudo iniciar sesión. Intente nuevamente.',
            confirmButtonColor: '#6d4c41'
          });
        }
      })
      .catch(error => {
        console.error('Error:', error);
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: 'Ocurrió un error al procesar la solicitud. Intente nuevamente.',
          confirmButtonColor: '#6d4c41'
        });
      });
  });
  } else {
    console.error('No se encontró el formulario en el documento');
  }
});