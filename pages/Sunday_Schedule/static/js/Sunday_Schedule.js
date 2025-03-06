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

// ##########################################################################


    scheduleButtons.forEach(button => {
        button.addEventListener('click', async () => {
            const classId = button.dataset.classId; // מזהה השיעור

            // שליפת זמן שנותר לשיעור
            const timeResponse = await fetch(`/Sunday_Schedule/time_until/${classId}`);
            const timeData = await timeResponse.json();

            // שליפת סטטוס השיעור והאם המשתמשת רשומה
            const statusResponse = await fetch(`/Sunday_Schedule/class_status/${classId}`);
            const statusData = await statusResponse.json();

            selectedSession = button;
            popupContent.innerText = button.dataset.popup;

            // בהתחלה מסתירים את כל הכפתורים
            registerBtn.style.display = 'none';
            waitlistBtn.style.display = 'none';
            cancelBtn.style.display = 'none';

            // אם השיעור כבר עבר
            if (timeData.expired) {
                popupContent.innerText = '⏳ זמן השיעור עבר!';
            } else {
                popupContent.innerText += `\n🕒 ${timeData.timeLeft}`;

                // בודקים האם המשתמשת רשומה לשיעור
                const userRegistered = statusData.userRegistered;
                const spotsLeft = statusData.spotsLeft;

                if (userRegistered) {
                    // אם המשתמשת רשומה לשיעור - הצג ביטול וסגירה
                    cancelBtn.style.display = 'block';
                } else {
                    // אם המשתמשת לא רשומה
                    if (spotsLeft > 0) {
                        // אם יש מקום בשיעור - הצג הרשמה וסגירה
                        registerBtn.style.display = 'block';
                    } else {
                        // אם אין מקום - הצג כניסה להמתנה וסגירה
                        waitlistBtn.style.display = 'block';
                    }
                }
            }

            popup.style.display = 'block';
            overlay.style.display = 'block';
        });
    });


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


    // איתור רכיבי הפופאפ לביטול הרשמה
    const cancelPopup = document.getElementById('cancel-popup');
    const cancelMessage = document.getElementById('cancel-message');
    const confirmCancelBtn = document.getElementById('confirm-cancel-btn');
    const closeCancelPopup = document.getElementById('close-cancel-popup');

    // ✅ טיפול בלחיצה על כפתור ביטול הרשמה
    cancelBtn.addEventListener("click", async () => {
        console.log("❌ שגיאה: אין שיעור נבחר.");
        if (!selectedSession) return;

        const classId = selectedSession.dataset.classId;
        console.log(`📡 שליחת בקשת סטטוס ביטול עבור שיעור ID: ${classId}`);

        // בקשת סטטוס ביטול מהשרת
        const response = await fetch(`/Sunday_Schedule/cancel_status/${classId}`);
        const cancelData = await response.json();
        console.log("✅ קיבלנו תשובה משרת הסטטוס:", cancelData);
        // קביעת ההודעה בהתאם למידע שהתקבל מהשרת
        cancelMessage.innerText = cancelData.message;

        // הצגת הפופאפ
        cancelPopup.style.display = 'block';
        overlay.style.display = 'block';

        // האזנה ללחיצה על כפתור הביטול הסופי
        confirmCancelBtn.onclick = () => handleCancelClass(classId);
    });

    // סגירת פופאפ הביטול
    closeCancelPopup.addEventListener("click", () => {
        cancelPopup.style.display = 'none';
        overlay.style.display = 'none';
    });

    function handleCancelClass(classId) {
        fetch(`/Sunday_Schedule/cancel`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({class_id: classId})
        })
            .then(response => response.json())
            .then(data => {
                alert(data.message); // הצגת הודעה מהשרת

                if (data.status === "success") {
                    // 🔴 תחילה סגירת הפופאפ של הביטול
                    cancelPopup.style.display = 'none';

                    // 🔴 עיכוב קצר של 300ms ואז סגירת הפופאפ הראשי
                    setTimeout(() => {
                        popup.style.display = 'none';
                        overlay.style.display = 'none';
                    }, 300);

                    // 🔄 עדכון מספר המשתמשות בשיעור
                    updateSpotsFromServer(classId);
                }
            })
            .catch(error => console.error("❌ שגיאה בביטול:", error));
    }

})
;

