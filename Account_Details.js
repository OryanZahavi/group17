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
        const firstNameInput = document.getElementById('firstName');

        // אימות שם פרטי
        if (!formInputs.firstName.value.trim()) {
            formInputs.firstName.classList.add('error');
            isValid = false;
        } else {
            formInputs.firstName.classList.remove('error');
        }

        //
        // // אימות שם משפחה
        // if (!formInputs.lastName.value.trim()) {
        //     alert("יש להזין שם משפחה.");
        //     isValid = false;
        // }
        //
        // // אימות תאריך לידה
        // if (!formInputs.birthDate.value) {
        //     alert("יש להזין תאריך לידה.");
        //     isValid = false;
        // } else if (!validateAge(formInputs.birthDate.value)){
        //     alert("מצטערים, ההצטרפות הינה מגיל 18 ומעלה.");
        //     isValid = false;
        // }
        //
        //
        // // אימות מייל
        // if (!validateEmail(formInputs.email.value)) {
        //     alert("נא להכניס כתובת מייל תקינה.");
        //     isValid = false;
        // }
        //
        // // אימות מספר פלאפון
        // if (!validatePhone(formInputs.phone.value)) {
        //     alert("נא להכניס מספר פלאפון תקין.");
        //     isValid = false;
        // }
        //
        // // אימות סיסמה
        // const passwordValidationResult = validatePassword(formInputs.password.value);
        // if (!passwordValidationResult.valid) {
        //     alert(passwordValidationResult.errorMessage);
        //     isValid = false;
        // }

        // אם הכל תקין - מציג את הפופ-אפ
        if (isValid) {
            popup.style.display = "block"; // מציג את הפופ-אפ
        }
    });

    // פונקציה לאימות מייל
    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    // פונקציה לאימות פלאפון
    function validatePhone(phone) {
        const re = /^0[0-9]{9}$/; // חייב להתחיל באפס ואחריו 9 ספרות
        return re.test(phone);
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
    // function validateAge(birthDate) {
    // const today = new Date();
    // const birthDateObj = new Date(birthDate);
    //
    // // בדיקת תאריך תקין
    // if (isNaN(birthDateObj.getTime())) {
    //     throw new Error("Invalid date format. Please use YYYY-MM-DD.");
    // }
    //
    // const age = today.getFullYear() - birthDateObj.getFullYear();
    // const monthDifference = today.getMonth() - birthDateObj.getMonth();
    //
    // // בודק אם היום בשנה לפני תאריך הלידה
    // if (monthDifference < 0 || (monthDifference === 0 && today.getDate() < birthDateObj.getDate())) {
    //     return age - 1 >= 18; // פחות מגיל 18
    // }
    // return age >= 18;
    // }

});
