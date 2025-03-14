document.addEventListener("DOMContentLoaded", function () {
    const formInputs = {
        old_password: document.querySelector("input[name='old_password']"),
        new_password: document.querySelector("input[name='new_password']"),
        confirm_password: document.querySelector("input[name='confirm_password']"),
    };

    const submitButton = document.getElementById("submit-button");
    const form = document.getElementById("edit-password-form"); // Get the form element

    submitButton.addEventListener("click", function (event) {
        event.preventDefault(); // Prevent default form submission
        let isValid = true;

        // Validate old_password (non-empty)
        const oldPasswordInput = formInputs.old_password;
        const oldPasswordError = document.getElementById("old_passwordError");
        if (!oldPasswordInput.value.trim()) {
            showError(oldPasswordInput, "יש להזין את הסיסמה הנוכחית.");
            isValid = false;
        } else {
            clearError(oldPasswordInput);
        }

        // Validate new_password (strong password)
        const newPasswordInput = formInputs.new_password;
        const newPasswordError = document.getElementById("new_passwordError");
        const passwordValidation = validatePassword(newPasswordInput.value.trim());
        if (!newPasswordInput.value.trim()) {
            showError(newPasswordInput, "יש להזין סיסמה חדשה.");
            isValid = false;
        } else if (!passwordValidation.valid) {
            showError(newPasswordInput, passwordValidation.errorMessage);
            isValid = false;
        } else {
            clearError(newPasswordInput);
        }

        // Validate confirm_password (non-empty)
        const confirmPasswordInput = formInputs.confirm_password;
        const confirmPasswordError = document.getElementById("confirm_passwordError");
        if (!confirmPasswordInput.value.trim()) {
            showError(confirmPasswordInput, "יש לאמת את הסיסמה החדשה.");
            isValid = false;
        } else {
            clearError(confirmPasswordInput);
        }

        // Validate confirm_password (matches new_password)
        if (!confirmPasswordInput.value.trim()) {
            showError(confirmPasswordInput, "יש לאמת את הסיסמה החדשה.");
            isValid = false;
        } else if (confirmPasswordInput.value !== newPasswordInput.value) {
            showError(confirmPasswordInput, "הסיסמאות אינן תואמות.");
            isValid = false;
        } else {
            clearError(confirmPasswordInput);
        }

        // If all validations pass, submit the form
        if (isValid) {
            form.submit(); // Programmatically submit the form
        }
    });

    // Function to validate a strong password
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

    // Function to show an error message for an input
    function showError(inputElement, message) {
        let errorElement = inputElement.nextElementSibling; // Assuming the error span is directly after the input
        errorElement.textContent = message;
        errorElement.classList.add("visible"); // Add visible class for styling
        inputElement.classList.add("error"); // Add error class for styling
    }

    // Function to clear an error message for an input
    function clearError(inputElement) {
        let errorElement = inputElement.nextElementSibling; // Assuming the error span is directly after the input
        errorElement.textContent = "";
        errorElement.classList.remove("visible"); // Remove visible class for styling
        inputElement.classList.remove("error"); // Remove error class for styling
    }
});
