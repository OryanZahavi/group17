document.addEventListener("DOMContentLoaded", function () {
    const formInputs = {
        firstName: document.querySelector("input[name='user_FirstName']"),
        lastName: document.querySelector("input[name='user_LastName']"),
        email: document.querySelector("input[name='user_Email']"),
        phone: document.querySelector("input[name='user_PhoneNumber']"),
        description: document.querySelector("textarea[name='Description']")
    };

    const submitButton = document.getElementById("submit-button");
    const lettersOnlyPattern = /^[A-Za-z\u0590-\u05FF]+$/;

    submitButton.addEventListener("click", function (event) {
        event.preventDefault(); // מונע שליחה של הטופס כברירת מחדל
        let isValid = true;

        // אימות שם פרטי
        const firstNameInput = document.getElementById("firstName");
        const firstNameError = document.getElementById("firstNameError");

        if (!firstNameInput.value.trim()) {
            firstNameError.textContent = "יש להזין שם פרטי.";
            firstNameError.classList.add("visible");
            firstNameInput.classList.add("error");
            isValid = false;
        } else if (!lettersOnlyPattern.test(firstNameInput.value.trim())) {
            firstNameError.textContent = "שם פרטי חייב להכיל אותיות בלבד.";
            firstNameError.classList.add("visible");
            firstNameInput.classList.add("error");
            isValid = false;
        } else {
            firstNameError.classList.remove("visible");
            firstNameInput.classList.remove("error");
        }

        // אימות שם משפחה
        const lastNameInput = document.getElementById("lastName");
        const lastNameError = document.getElementById("lastNameError");
        if (!lastNameInput.value.trim()) {
            lastNameError.textContent = "יש להזין שם משפחה.";
            lastNameError.classList.add("visible");
            lastNameInput.classList.add("error");
            isValid = false;
        } else if (!lettersOnlyPattern.test(lastNameInput.value.trim())) {
            lastNameError.textContent = "שם משפחה חייב להכיל אותיות בלבד.";
            lastNameError.classList.add("visible");
            lastNameInput.classList.add("error");
            isValid = false;
        } else {
            lastNameError.classList.remove("visible");
            lastNameInput.classList.remove("error");
        }

        // אימות מייל
        const emailInput = document.getElementById("email");
        const emailError = document.getElementById("emailError");
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

        // אימות מספר פלאפון
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

        // אימות תיאור הפנייה
        const descriptionInput = formInputs.description;
        const descriptionError = document.getElementById("descriptionError");
        const descriptionValue = descriptionInput.value.trim();

        if (!descriptionValue) {
            descriptionError.textContent = "יש להזין תיאור פנייה.";
            descriptionError.classList.add("visible");
            descriptionInput.classList.add("error");
            isValid = false;
        } else if (descriptionValue.length < 10) {
            descriptionError.textContent = "תיאור הפנייה חייב להכיל לפחות 10 תווים.";
            descriptionError.classList.add("visible");
            descriptionInput.classList.add("error");
            isValid = false;
        } else {
            descriptionError.classList.remove("visible");
            descriptionInput.classList.remove("error");
        }

        // אם הכל תקין - מציג את הפופ-אפ
        if (isValid) {
            popup.style.display = "block"; // מציג את הפופ-אפ
        }
    });

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
});
