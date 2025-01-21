function loadUserDetails() {
    const userDetails = JSON.parse(localStorage.getItem("userDetails"));
    if (userDetails) {
        document.getElementById("display_FirstName").innerText = userDetails.firstName;
        document.getElementById("display_LastName").innerText = userDetails.lastName;
        document.getElementById("display_BirthDate").innerText = userDetails.birthDate;
        document.getElementById("display_Email").innerText = userDetails.email;
        document.getElementById("display_Phone").innerText = userDetails.phone;
    } else {
        alert("לא נמצאו פרטים");
    }
}

// טוען את פרטי המשתמש בעת טעינת הדף
window.onload = loadUserDetails;