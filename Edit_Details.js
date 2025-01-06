document.addEventListener("DOMContentLoaded", function () {
    const submitButton = document.getElementById("submit-button");
    const popup = document.getElementById("popup");

    // הצגת הפופאפ בעת לחיצה על "אישור שינויים"
    submitButton.addEventListener("click", function (event) {
        event.preventDefault(); // מונע שליחה של הטופס
        popup.style.display = "block"; // מציג את החלון
    });
});
