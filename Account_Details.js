document.addEventListener("DOMContentLoaded", function () {
    const formInputs = {
        firstName: document.querySelector("input[name='user_FirstName']"),
        lastName: document.querySelector("input[name='user_LastName']"),
        birthDate: document.querySelector("input[name='user_Date']"),
        email: document.querySelector("input[name='user_Email']"),
        phone: document.querySelector("input[name='user_Phone']"),
        password: document.querySelector("input[name='user_Password']"),
    };

    const submitButton = document.getElementById("submit-button");
    const popup = document.getElementById("popup");

    submitButton.addEventListener("click", function (event) {
        event.preventDefault(); // מונע שליחה של הטופס כברירת מחדל

        let isValid = true;

        // אימות שם פרטי
        //const firstNameInput = document.getElementById('firstName');
        //
        //        // אימות שם פרטי
        //        if (!formInputs.firstName.value.trim()) {
        //            formInputs.firstName.classList.add('error');
        //            isValid = false;
        //        } else {
        //            formInputs.firstName.classList.remove('error');
        //        }

        //
        // אימות שם משפחה
        const firstNameInput = document.getElementById("firstName");
        const firstNameError = document.getElementById("firstNameError");
        if (!firstNameInput.value.trim()) {
            firstNameError.classList.add("visible"); // Show the error message
            firstNameInput.classList.add("error"); // Add error style to input
            isValid = false;
        } else {
            firstNameError.classList.remove("visible"); // Hide the error message
            firstNameInput.classList.remove("error"); // Remove error style
        }

        // אימות שם משפחה
        const lastNameInput = document.getElementById("lastName");
        const lastNameError = document.getElementById("lastNameError");
        if (!lastNameInput.value.trim()) {
            lastNameError.classList.add("visible"); // Show the error message
            lastNameInput.classList.add("error"); // Add error style to input
            isValid = false;
        } else {
            lastNameError.classList.remove("visible"); // Hide the error message
            lastNameInput.classList.remove("error"); // Remove error style
        }


         // אימות תאריך לידה
        const birthDateInput = document.getElementById("birthDate");
        const birthDateError = document.getElementById("birthDateError");
        const birthDateValue = birthDateInput.value.trim();
        if (!birthDateValue) {
            // Case: No input
            birthDateError.textContent = "יש להזין תאריך לידה.";
            birthDateError.classList.add("visible");
            birthDateInput.classList.add("error");
            isValid = false;
        } else if (!validateAge(birthDateValue)) {
            // Case: Invalid date or underage
            birthDateError.textContent = "עליך להיות מעל גיל 18.";
            birthDateError.classList.add("visible");
            birthDateInput.classList.add("error");
            isValid = false;
        } else {
            birthDateError.classList.remove("visible");
            birthDateInput.classList.remove("error");
        }


        // // אימות מייל
        const emailInput = document.getElementById("email");
        const emailError = document.getElementById("emailError");
        const emailValue = emailInput.value.trim();
        if (!emailValue) {
            // Case: No input
            emailError.textContent = "יש להזין כתובת דוא\"ל.";
            emailError.classList.add("visible");
            emailInput.classList.add("error");
            isValid = false;
        } else if (!isValidEmail(emailValue)) {
            // Case: Invalid email
            emailError.textContent = "כתובת הדוא\"ל אינה תקינה.";
            emailError.classList.add("visible");
            emailInput.classList.add("error");
            isValid = false;
        } else {
            emailError.classList.remove("visible");
            emailInput.classList.remove("error");
        }


        // // אימות מספר פלאפון
        const phoneInput = document.getElementById("phoneNumber");
        const phoneError = document.getElementById("phoneNumberError");
        const phoneValue = phoneInput.value.trim();

        if (!phoneValue) {
            phoneError.textContent = "יש להזין מספר טלפון.";
            phoneError.classList.add("visible");
            phoneInput.classList.add("error");
            isValid = false;
        } else if (!isValidIsraeliPhone(phoneValue)) {
            phoneError.textContent = "מספר הטלפון שהוזן אינו תקין.";
            phoneError.classList.add("visible");
            phoneInput.classList.add("error");
            isValid = false;
        } else {
            phoneError.classList.remove("visible");
            phoneInput.classList.remove("error");
        }


        // // אימות סיסמה
        const passwordInput = document.getElementById("password");
        const passwordError = document.getElementById("passwordError");
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

        //אימות קובץ
//        const fileInput = document.getElementById("Hfile");
//        const fileError = document.getElementById("fileError");
//        let isValid = true;
//
//        fileInput.addEventListener("change", function() {
//            fileError.textContent = ""; // Clear previous error message
//            fileInput.classList.remove("error"); // Remove previous error styling
//
//            if (!fileInput.files || fileInput.files.length === 0) {
//                fileError.textContent = "יש לבחור קובץ.";
//                fileError.classList.add("visible");
//                fileInput.classList.add("error");
//                isValid = false;
//            } else {
//                // Additional validations can be added here if needed
//            }
//        });

        // אם הכל תקין - מציג את הפופ-אפ
        if (isValid) {
            popup.style.display = "block"; // מציג את הפופ-אפ
        }
    });

//    פונקציה לאימות גיל (מעל 18)
    function validateAge(birthDate) {
        const today = new Date();
        const birthDateObj = new Date(birthDate);
        const age = today.getFullYear() - birthDateObj.getFullYear();
        const monthDifference = today.getMonth() - birthDateObj.getMonth();

        // בודק אם היום בשנה לפני תאריך הלידה
        if (monthDifference < 0 || (monthDifference === 0 && today.getDate() < birthDateObj.getDate())) {
            return age - 1 >= 18; // פחות מגיל 18
        }
        return age >= 18;
    }

    // פונקציה לאימות מייל
    function isValidEmail(email) {
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailPattern.test(email);
    }

    // פונקציה לאימות מספר טלפון ישראלי
    function isValidIsraeliPhone(phone) {
        const phonePattern = /^(?:\+972|0)(?:[23489]|5[0-9])-?\d{7}$/;
        return phonePattern.test(phone);
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
