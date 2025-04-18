document.getElementById("form").addEventListener("submit", function (event) {
    event.preventDefault();

    document.getElementById("emailError").textContent = "";
    document.getElementById("passwordError").textContent = "";
    document.getElementById("accountTypeError").textContent = "";

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();
    const accountType = document.getElementById("accountType").value;

    const emailRegex = /^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$/i;
    const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$/;

    let valid = true;

    if (!email) {
        document.getElementById("emailError").textContent = "El correo es obligatorio.";
        valid = false;
    } else if (!emailRegex.test(email)) {
        document.getElementById("emailError").textContent = "Ingrese un correo válido.";
        valid = false;
    }

    if (!password) {
        document.getElementById("passwordError").textContent = "La contraseña es obligatoria.";
        valid = false;
    } else if (!passwordRegex.test(password)) {
        document.getElementById("passwordError").textContent = "Debe tener al menos 6 caracteres, una letra y un número.";
        valid = false;
    }

    if (!accountType) {
        document.getElementById("accountTypeError").textContent = "Seleccione el tipo de cuenta.";
        valid = false;
    }

    if (valid) {
        if (accountType === "Administrador") {
            window.location.href = urlAdministrador;
        } else {
            window.location.href = urlusuario;
        }
    }
});
