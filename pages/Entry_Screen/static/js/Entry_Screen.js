document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form"); // הטופס כולו
    const emailInput = document.getElementById("email");
    const emailError = document.getElementById("emailError");
    const passwordInput = document.getElementById("password");
    const passwordError = document.getElementById("passwordError");
    const submitButton = document.getElementById("submit-button");
    // form.addEventListener("submit", function (event) {
    //     let isValid = true;
    submitButton.addEventListener("click", function (event) {
        event.preventDefault();  // מונע שליחה רגילה
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

        if (!passwordValue) {
            passwordError.textContent = "יש להזין סיסמה.";
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


    // 📨 **שליחת הבקשה לשרת**
        fetch("/Entry_Screen", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
           body: new URLSearchParams({ user_Email: emailValue, user_Password: passwordValue })  // שליחת הנתונים בפורמט נכון
        })
       .then(response => {
            if (!response.ok) {
                throw new Error("שגיאת שרת");
            }
            return response.text();  // כי Flask מחזיר `redirect()`
        })
        .then(data => {
            console.log("🔄 מעבר לדף הבית...");
            window.location.href = "/Home_Page";  // עדכון הכתובת לפי Flask
        })
        .catch(error => console.error("❌ שגיאת תקשורת:", error));

});
    // פונקציה לאימות מייל
    function isValidEmail(email) {
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailPattern.test(email);
    }

});

document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");

    form.addEventListener("submit", function (event) {
        event.preventDefault();  // מונע שליחת טופס רגילה

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        fetch("/api/login", {  // קריאה ל-API Flask
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({user_Email: email, user_Password: password})  // שליחת JSON
        })
            .then(response => response.json())  // הפיכת התשובה לאובייקט JSON
            .then(data => {
                if (data.status === "success") {
                    window.location.href = data.redirect;  // מעבר לדף הבית
                } else {
                    alert(data.message);  // הצגת הודעת שגיאה
                }
            })
            .catch(error => console.error("Error:", error));
    });
});

