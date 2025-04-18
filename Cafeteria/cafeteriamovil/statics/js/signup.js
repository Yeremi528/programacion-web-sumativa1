document.getElementById("form").addEventListener("submit", function(event) {
    event.preventDefault();

    // Limpiar errores
    document.getElementById("nameError").textContent = "";
    document.getElementById("apellidoError").textContent = "";
    document.getElementById("emailError").textContent = "";
    document.getElementById("passwordError").textContent = "";
    document.getElementById("accountTypeError").textContent = "";

    // Obtener datos
    const name = document.getElementById("name").value.trim();
    const apellido = document.getElementById("apellido").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();
    const accountType = document.getElementById("accountType").value;

    // Formatos aceptados 
    const nameRegex = /^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$/;
    const emailRegex = /^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$/i;
    const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$/;

    let valid = true;

    // Verificación nombre
    if (!name) {
        document.getElementById("nameError").textContent = "El nombre es obligatorio.";
        valid = false;
    } else if (!nameRegex.test(name)) {
        document.getElementById("nameError").textContent = "El nombre solo puede contener letras.";
        valid = false;
    }

    // Verificación apellido
    if (!apellido) {
        document.getElementById("apellidoError").textContent = "El apellido es obligatorio.";
        valid = false;
    } else if (!nameRegex.test(apellido)) {
        document.getElementById("apellidoError").textContent = "El apellido solo puede contener letras.";
        valid = false;
    }

    // Verificación email
    if (!email) {
        document.getElementById("emailError").textContent = "El correo es obligatorio.";
        valid = false;
    } else if (!emailRegex.test(email)) {
        document.getElementById("emailError").textContent = "Ingrese un correo válido.";
        valid = false;
    }

    // Verificación contraseña
    if (!password) {
        document.getElementById("passwordError").textContent = "La contraseña es obligatoria.";
        valid = false;
    } else if (!passwordRegex.test(password)) {
        document.getElementById("passwordError").textContent = "Debe tener al menos 6 caracteres, una letra y un número.";
        valid = false;
    }

    // Verificación tipo de cuenta
    if (!accountType) {
        document.getElementById("accountTypeError").textContent = "Seleccione el tipo de cuenta.";
        valid = false;
    }

    // Si todo es válido
    if (valid) {
        alert ("Se ah creado tu cuenta con exito");

        if (accountType === "Administrador") {
            window.location.href = urlAdministrador;
        } else {
            window.location.href = urlusuario;
        }
    }
});
