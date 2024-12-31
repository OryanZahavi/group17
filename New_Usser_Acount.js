 function saveUserDetails() {
        const userDetails = {
            firstName: document.getElementById("user_FirstName").value,
            lastName: document.getElementById("user_LastName").value,
            birthDate: document.getElementById("user_Date").value,
            email: document.getElementById("user_Email").value,
            phone: document.getElementById("user_Phone").value,
            password: document.getElementById("user_Password").value,
        };

        localStorage.setItem("userDetails", JSON.stringify(userDetails));
        alert("הפרטים נשמרו בהצלחה!");
        window.location.href = "My_Account.html"; // מעבר לדף הפרטים
    }