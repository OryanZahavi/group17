document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("login-form");
    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");
    const emailError = document.getElementById("email-error");
    const passwordError = document.getElementById("password-error");

    form.addEventListener("submit", function (e) {
        let valid = true;

        // ולידציה לשדה מייל
        if (!validateEmail(emailInput.value)) {
            emailError.textContent = "נא להכניס כתובת מייל תקינה.";
            emailError.style.display = "block";
            valid = false;
        } else {
            emailError.style.display = "none";
        }

        // ולידציה לשדה סיסמה
        const passwordValidationResult = validatePassword(passwordInput.value);
        if (!passwordValidationResult.valid) {
            passwordError.textContent = passwordValidationResult.errorMessage;
            passwordError.style.display = "block";
            valid = false;
        } else {
            passwordError.style.display = "none";
        }

        if (!valid) {
            e.preventDefault(); // מונע שליחה אם לא תקין
        }
    });

    // פונקציה לוולידציית מייל
    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    // פונקציה לוולידציית סיסמה
    function validatePassword(password) {
        if (password.length < 6) {
            return { valid: false, errorMessage: "הסיסמה חייבת להכיל לפחות 6 תווים." };
        }
        if (!/[A-Z]/.test(password)) {
            return { valid: false, errorMessage: "הסיסמה חייבת להכיל לפחות אות גדולה באנגלית." };
        }
        if (!/[0-9]/.test(password)) {
            return { valid: false, errorMessage: "הסיסמה חייבת להכיל לפחות מספר אחד." };
        }
        if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
            return { valid: false, errorMessage: "הסיסמה חייבת להכיל לפחות סימן מיוחד (כמו !, @, #)." };
        }
        return { valid: true, errorMessage: "" };
    }
});
