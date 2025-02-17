
document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form"); // הטופס כולו
    const emailInput = document.getElementById("email");
    const emailError = document.getElementById("emailError");
    const passwordInput = document.getElementById("password");
    const passwordError = document.getElementById("passwordError");
    const submitButton = document.querySelector("input[type='submit']"); // בחירת הכפתור הנכון

    form.addEventListener("submit", function (event) {
        let isValid = true;

        // אימות מייל
        const emailValue = emailInput.value.trim();
        if (!emailValue) {
            emailError.textContent = "יש להזין כתובת דוא\"ל.";
            emailError.classList.add("visible");
            emailInput.classList.add("error");
            isValid = false;
        } else if (!isValidEmail(emailValue)) {
            emailError.textContent = "כתובת הדוא\"ל אינה תקינה.";
            emailError.classList.add("visible");
            emailInput.classList.add("error");
            isValid = false;
        } else {
            emailError.classList.remove("visible");
            emailInput.classList.remove("error");
        }

        // אימות סיסמה
        const passwordValue = passwordInput.value.trim();
        const passwordValidation = validatePassword(passwordValue);

        if (!passwordValue) {
            passwordError.textContent = "יש להזין סיסמה.";
            passwordError.classList.add("visible");
            passwordInput.classList.add("error");
            isValid = false;
        } else if (!passwordValidation.valid) {
            passwordError.textContent = passwordValidation.errorMessage;
            passwordError.classList.add("visible");
            passwordInput.classList.add("error");
            isValid = false;
        } else {
            passwordError.classList.remove("visible");
            passwordInput.classList.remove("error");
        }

        // מניעת שליחה במקרה של שגיאות
        if (!isValid) {
            event.preventDefault(); // רק אם יש שגיאות, מונעים שליחה לשרת
        }
    });

    // פונקציה לאימות מייל
    function isValidEmail(email) {
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailPattern.test(email);
    }

    // פונקציה לאימות סיסמה
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







//changes -30.1-

// document.addEventListener("DOMContentLoaded", function () {
//     const formInputs = {
//         email: document.querySelector("input[name='user_Email']"),
//         password: document.querySelector("input[name='user_Password']"),
//     };
//
//     const submitButton = document.getElementById("submit-button");
//
//     submitButton.addEventListener("click", function (event) {
//         event.preventDefault(); // מונע שליחה של הטופס כברירת מחדל
//         let isValid = true;
//
//        // // אימות מייל
//         const emailInput = document.getElementById("email");
//         const emailError = document.getElementById("emailError");
//         const emailValue = emailInput.value.trim();
//
//         // Detect language or define it (e.g., from user settings or page attribute)
//         const language = document.documentElement.lang || "he"; // Default to Hebrew
//
//         if (!emailValue) {
//             // Case: No input
//             emailError.textContent = "יש להזין כתובת דוא\"ל.";
//             emailError.classList.add("visible");
//             emailInput.classList.add("error");
//             isValid = false;
//         } else if (!isValidEmail(emailValue)) {
//             // Case: Invalid email
//             emailError.textContent = "כתובת הדוא\"ל אינה תקינה.";
//             emailError.classList.add("visible");
//             emailInput.classList.add("error");
//             isValid = false;
//         } else {
//             emailError.classList.remove("visible");
//             emailInput.classList.remove("error");
//         }
//
//          // אימות סיסמה
//         const passwordInput = document.getElementById("password");
//         const passwordError = document.getElementById("passwordError");
//         const passwordValue = passwordInput.value.trim();
//
//         const passwordValidation = validatePassword(passwordValue);
//
//         if (!passwordValue) {
//             passwordError.textContent = "יש להזין סיסמה.";
//             passwordError.classList.add("visible");
//             passwordInput.classList.add("error");
//             isValid = false;
//         } else if (!passwordValidation.valid) {
//             passwordError.textContent = passwordValidation.errorMessage;
//             passwordError.classList.add("visible");
//             passwordInput.classList.add("error");
//             isValid = false;
//         } else {
//             passwordError.classList.remove("visible");
//             passwordInput.classList.remove("error");
//         }
//
//         if (isValid) {
//              window.location.href = "Home_Page.html";
//         }
//     });
//
//     // פונקציה לאימות מייל
//     function isValidEmail(email) {
//         const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
//         return emailPattern.test(email);
//     }
//
//    // פונקציה לאימות סיסמה
//     function validatePassword(password) {
//         if (password.length < 6) {
//             return { valid: false, errorMessage: "הסיסמה חייבת להכיל לפחות 6 תווים." };
//         }
//         if (!/[A-Z]/.test(password)) {
//             return { valid: false, errorMessage: "הסיסמה חייבת להכיל לפחות אות גדולה באנגלית." };
//         }
//         if (!/[0-9]/.test(password)) {
//             return { valid: false, errorMessage: "הסיסמה חייבת להכיל לפחות מספר אחד." };
//         }
//         if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
//             return { valid: false, errorMessage: "הסיסמה חייבת להכיל לפחות סימן מיוחד (כמו !, @, #)." };
//         }
//         return { valid: true, errorMessage: "" };
//     }
// });
