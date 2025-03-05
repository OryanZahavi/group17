document.addEventListener("DOMContentLoaded", function () {
    //     //---------------------סידור הכפתורים של ימות השבוע+ עדכון שלהם בכל יום חמישי ב 22:00 --------------------
    const days = ['חמישי', 'רביעי', 'שלישי', 'שני', 'ראשון'];

    function calculateWeekStart() {
        const now = new Date();
        const currentDay = now.getDay();
        if (currentDay === 4 && now.getHours() >= 22) {
            now.setDate(now.getDate() + 1);
        }
        const firstDayOfWeek = new Date(now);
        firstDayOfWeek.setDate(firstDayOfWeek.getDate() - currentDay);
        return firstDayOfWeek;
    }

    function updateDates() {
        const weekStart = calculateWeekStart();
        const weekDates = [];
        for (let i = 0; i < 5; i++) {
            const date = new Date(weekStart);
            date.setDate(weekStart.getDate() + i);
            weekDates.push(date);
        }
        const reversedWeekDates = weekDates.reverse();
        const buttons = document.querySelectorAll('.dates button');
        buttons.forEach((button, index) => {
            const formattedDate = reversedWeekDates[index].toLocaleDateString('he-IL', {
                day: 'numeric', month: 'long',
            });
            button.innerHTML = `${formattedDate}<br>${days[index]}`;
            button.dataset.date = reversedWeekDates[index].toISOString().split('T')[0];
        });
    }

    updateDates();

    const scheduleButtons = document.querySelectorAll('.schedule .session');
    const popup = document.getElementById('popup');
    const overlay = document.querySelector('.overlay');
    const popupContent = document.getElementById('popup-content');
    const registerBtn = document.getElementById('register-btn');
    const waitlistBtn = document.getElementById('waitlist-btn');
    const cancelBtn = document.getElementById('cancel-btn');
    const closePopup = document.getElementById('close-popup');
    let selectedSession;

    overlay.addEventListener('click', closePopupHandler);
    closePopup.addEventListener('click', closePopupHandler);

    function closePopupHandler() {
        popup.style.display = 'none';
        overlay.style.display = 'none';
    }


scheduleButtons.forEach(button => {
    button.addEventListener('click', () => {
        selectedSession = button;
        const sessionId = button.dataset.classId;

        fetch(`/Sunday_Schedule/class_status/${sessionId}`)
            .then(response => response.json())
            .then(data => {
                console.log("🔍 נתונים שהתקבלו מהשרת:", data);

                if (!data || !data.datetime) {
                    console.error("❌ שגיאה: השדה datetime לא קיים בתגובה מהשרת");
                    alert("שגיאה בטעינת נתוני השיעור. אנא נסה שוב.");
                    return;
                }

                if (data.status === "expired") {
                    popupContent.innerText = "⏳ זמן הביטול עבר!";
                    registerBtn.style.display = 'none';
                    waitlistBtn.style.display = 'none';
                    cancelBtn.style.display = 'none';
                    popup.style.display = 'block';
                    overlay.style.display = 'block';
                    return;
                }

                // מציגים את הפופ-אפ הרגיל אם השיעור עדיין תקף
                popupContent.innerText = button.dataset.popup;
                registerBtn.style.display = 'block';
                waitlistBtn.style.display = 'none';
                cancelBtn.style.display = 'block';

                if (data.spotsLeft > 0) {
                    waitlistBtn.style.display = 'none'; // אם יש מקום פנוי - מסתירים רשימת המתנה
                } else {
                    registerBtn.style.display = 'none'; // השיעור מלא - מסתירים כפתור הרשמה
                    waitlistBtn.style.display = 'block'; // מציגים את כפתור רשימת ההמתנה
                }

                popup.style.display = 'block';
                overlay.style.display = 'block';
            })
            .catch(error => console.error("Error fetching class status:", error));
    });
});
    // scheduleButtons.forEach(button => {
    //     button.addEventListener('click', () => {
    //         selectedSession = button;
    //         const sessionId = button.dataset.classId;
    //
    //         popupContent.innerText = button.dataset.popup;
    //         registerBtn.style.display = 'block';
    //         waitlistBtn.style.display = 'none';  // בהתחלה מסתירים את כפתור רשימת ההמתנה
    //         cancelBtn.style.display = 'block';
    //
    //         fetch(`/Sunday_Schedule/class_status/${sessionId}`)
    //             .then(response => {
    //                 if (!response.ok) {
    //                     throw new Error("Failed to fetch class status");
    //                 }
    //                 return response.json();
    //             })
    //             .then(data => {
    //                 if (data.spotsLeft !== undefined) {
    //                     if (data.spotsLeft > 0) {
    //                         waitlistBtn.style.display = 'none'; // אם יש מקום פנוי - מסתירים רשימת המתנה
    //                     } else {
    //                         registerBtn.style.display = 'none'; // השיעור מלא - מסתירים כפתור הרשמה
    //                         waitlistBtn.style.display = 'block'; // מציגים את כפתור רשימת ההמתנה
    //                     }
    //                 } else {
    //                     console.error("Invalid response format:", data);
    //                 }
    //             })
    //             .catch(error => console.error("Error fetching class status:", error));
    //
    //
    //         popup.style.display = 'block';
    //         overlay.style.display = 'block';
    //     });
    // });



// עובד!! 5.3
    // פונקציה שמעדכנת את מספר המשתתפים לפי נתוני השרת
    function updateSpotsFromServer(sessionId) {
        fetch(`/Sunday_Schedule/class_status/${sessionId}`)
            .then(response => response.json())
            .then(data => {
                if (data.spotsLeft !== undefined) {
                    const spotsElement = document.getElementById(`spots-${sessionId}`);
                    if (spotsElement) {
                        spotsElement.textContent = `${data.spotsFilled}/${data.capacity} רשומות`;
                    }
                }
            })
            .catch(error => console.error("Error updating spots:", error));
    }




function sendRequest(endpoint, sessionId) {
    fetch(`/Sunday_Schedule${endpoint}`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({class_id: sessionId})
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        if (data.status === "success") {
            updateSpotsFromServer(sessionId);
        }
    })
    .catch(error => console.error("Error:", error));
}


// עובד!
registerBtn.addEventListener('click', () => {
    sendRequest('/register', selectedSession.dataset.classId);
    closePopupHandler();
});


waitlistBtn.addEventListener('click', () => {
    sendRequest('/waitlist', selectedSession.dataset.classId);
    closePopupHandler();
});

cancelBtn.addEventListener("click", () => {
    if (!selectedSession) return;

    const sessionId = selectedSession.dataset.classId;

    fetch(`/Sunday_Schedule/cancel`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ class_id: sessionId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "error") {
            alert(data.message);
        } else if (data.status === "warning") {
            const confirmPayment = confirm("שימי לב: ביטול כרוך בתשלום. האם לבטל?");
            if (confirmPayment) {
                sendRequest("/Sunday_Schedule/cancel", sessionId);
            }
        } else if (data.status === "success") {
            alert(data.message);
            updateSpotsFromServer(sessionId);
        }
    })
    .catch(error => console.error("Error processing cancellation:", error));
});


// cancelBtn.addEventListener('click', () => {
//     sendRequest('/cancel', selectedSession.dataset.classId);
//     closePopupHandler();
// });


})
;

