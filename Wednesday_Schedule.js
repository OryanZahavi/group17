document.addEventListener("DOMContentLoaded", function () {

    //---------------------סידור הכפתורים של ימות השבוע+ עדכון שלהם בכל יום חמישי ב 22:00 --------------------

    const days = ['חמישי', 'רביעי', 'שלישי', 'שני', 'ראשון']; // ימות השבוע בעברית

    function calculateWeekStart() {
        const now = new Date();
        const currentDay = now.getDay(); // היום הנוכחי (0 = ראשון, 6 = שבת)

        // אם היום חמישי אחרי השעה 22:00, התחל את השבוע הבא
        if (currentDay === 4 && now.getHours() >= 22) {
            now.setDate(now.getDate() + 1); // תעבור ליום שישי
        }

        // חישוב יום ראשון הקרוב
        const firstDayOfWeek = new Date(now);
        firstDayOfWeek.setDate(firstDayOfWeek.getDate() - currentDay); // יום ראשון הקרוב
        return firstDayOfWeek;
    }

    // מעדכן את התאריכים
    function updateDates() {
        const weekStart = calculateWeekStart();

        // מחשבים את התאריכים של השבוע (ראשון עד חמישי)
        const weekDates = [];
        for (let i = 0; i < 5; i++) {
            const date = new Date(weekStart);
            date.setDate(weekStart.getDate() + i);
            weekDates.push(date);
        }

        // הופכים את סדר הימים כדי להתאים לסדר מימין לשמאל
        const reversedWeekDates = weekDates.reverse();

        // מעדכנים את הכפתורים
        const buttons = document.querySelectorAll('.dates button');
        buttons.forEach((button, index) => {
            const formattedDate = reversedWeekDates[index].toLocaleDateString('he-IL', {
                day: '2-digit',
                month: '2-digit',
            });

            button.innerHTML = `${formattedDate}<br>${days[index]}`;
            button.dataset.date = reversedWeekDates[index].toISOString().split('T')[0]; // שמירת תאריך כ-ID

            // הדגשה ליום רביעי
            if (days[index] === 'רביעי') {
                button.classList.add('active'); // הוספת מחלקה ליום רביעי
            } else {
                button.classList.remove('active'); // הסרת מחלקה מימים אחרים
            }
        });

    }

    updateDates();// עדכון הימים


//---------------------חישוב נקודת הזמן של כל שיעור --------------------


// פונקציה ליצירת תאריך מהמאפיינים data-day-offset ו-data-time
function generateDateFromAttributes(element) {
    if (!element || !element.dataset.time || !element.dataset.dayOffset) {
        console.error("Missing dataset attributes for element:", element);
        return null;
    }

    const weekStart = calculateWeekStart();
    const dayOffset = Number(element.dataset.dayOffset);
    const time = element.dataset.time.trim(); // לנקות רווחים

    if (!/^\d{2}:\d{2}$/.test(time)) {
        console.error("Invalid time format in data-time attribute:", time);
        return null;
    }

    const [hour, minute] = time.split(':').map(Number);
    const sessionDate = new Date(weekStart);
    sessionDate.setDate(sessionDate.getDate() + dayOffset);
    sessionDate.setHours(hour, minute, 0, 0);

    if (isNaN(sessionDate.getTime())) {
        console.error("Invalid sessionDate generated:", sessionDate);
        return null;
    }

    return sessionDate;
}
    const scheduleButtons = document.querySelectorAll('.schedule .session');
    const popup = document.getElementById('popup');
    const overlay = document.querySelector('.overlay');
    const popupContent = document.getElementById('popup-content');
    const registerBtn = document.getElementById('register-btn');
    const waitlistBtn = document.getElementById('waitlist-btn');
    const cancelBtn = document.getElementById('cancel-btn');
    const closePopup = document.getElementById('close-popup');
    const cancelPopup = document.getElementById('cancel-popup');
    const cancelTimer = document.getElementById('cancel-timer');
    const cancelWarning = document.getElementById('cancel-warning');
    const confirmCancelBtn = document.getElementById('confirm-cancel-btn');
    const closeCancelPopup = document.getElementById('close-cancel-popup');
    let cancelInterval; // טיימר לספירה לאחור


    let selectedSession; // משתנה לאחסון השיעור הנבחר

    // סגירת הפופ-אפ
    overlay.addEventListener('click', closePopupHandler);
    closePopup.addEventListener('click', closePopupHandler);

    function closePopupHandler() {
        popup.style.display = 'none';
        overlay.style.display = 'none';
    }

    // לחיצה על כפתור הרשמה
    registerBtn.addEventListener('click', () => {
        const spotsText = selectedSession.querySelector('.spots');
        const [current, max] = spotsText.textContent.split('/').map(Number);

        // תיקון התנאי להרשמה
        if (current < max) {
            spotsText.textContent = `${current + 1}/${max} רשומות`;
            alert('הרשמתך לשיעור אושרה!');
            closePopupHandler();
        } else {
            alert('לא ניתן להירשם, השיעור מלא.');
        }
    });

    // לחיצה על כפתור הרשמה
    registerBtn.addEventListener('click', () => {
        if (!selectedSession) return; // וודא שנבחר שיעור

        const spotsText = selectedSession.querySelector('.spots');
        const current = parseInt(spotsText.textContent.split('/')[0], 10); // מספר הרשומות הנוכחי

        if (current < 10) { // אם יש פחות מ-10 משתתפות
            spotsText.textContent = `${current + 1}/10 רשומות`;
            alert('הרשמתך לשיעור אושרה!');
            closePopupHandler();
        } else {
            alert('לא ניתן להירשם, השיעור מלא.');
        }
    });

    // לחיצה על כפתור כניסה לרשימת המתנה
    waitlistBtn.addEventListener('click', () => {
        if (!selectedSession) return; // וודא שנבחר שיעור

        const spotsText = selectedSession.querySelector('.spots');
        const current = parseInt(spotsText.textContent.split('/')[0], 10); // מספר הרשומות הנוכחי

        if (current >= 10) { // אם השיעור מלא
            alert('נוספת בהצלחה לרשימת ההמתנה!');
            closePopupHandler();
        } else {
            alert('יש מקומות פנויים, אנא הירשם לשיעור במקום.');
        }
    });

    // לחיצה על שיעור בלוח השיעורים
    scheduleButtons.forEach(button => {
        button.addEventListener('click', () => {
            const sessionDate = generateDateFromAttributes(button);
            const now = new Date();
            selectedSession = button; // שמירת השיעור שנבחר

            if (sessionDate < now) {
                popupContent.innerText = 'זמן השיעור עבר.';
                registerBtn.style.display = 'none';
                cancelBtn.style.display = 'none';
                waitlistBtn.style.display = 'none';
            } else {
                popupContent.innerText = button.dataset.popup;
                registerBtn.style.display = 'block';
                waitlistBtn.style.display = 'block';
                cancelBtn.style.display = 'block';
            }

            popup.style.display = 'block';
            overlay.style.display = 'block';
        });
    });

    // לחיצה על כפתור ביטול הרשמה
    cancelBtn.addEventListener('click', () => {
        if (!selectedSession) return;

        const sessionDate = generateDateFromAttributes(selectedSession);
        const now = new Date();
        const timeDifference = sessionDate - now; // חישוב ההבדל בזמן (מילישניות)

        if (timeDifference <= 0) {
            alert('לא ניתן לבטל, זמן השיעור עבר.');
            return;
        }
// סגירת הפופ-אפ הקודם
        closePopupHandler();


        // הצגת פופ-אפ ביטול הרשמה
        cancelPopup.style.display = 'block';
        overlay.style.display = 'block';

        // עדכון טיימר
        updateCancelTimer(sessionDate);

        // הפעלת טיימר שמעדכן כל שנייה
        cancelInterval = setInterval(() => {
            updateCancelTimer(sessionDate);
        }, 1000);
    });

    // עדכון טיימר בפופ-אפ
    function updateCancelTimer(sessionDate) {
        const now = new Date();
        const timeDifference = sessionDate - now; // חישוב ההבדל בזמן (מילישניות)

        if (timeDifference <= 0) {
            clearInterval(cancelInterval); // עצירת הטיימר
            cancelTimer.innerText = "זמן השיעור עבר.";
            return;
        }

        const hours = Math.floor(timeDifference / (1000 * 60 * 60));
        const minutes = Math.floor((timeDifference % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((timeDifference % (1000 * 60)) / 1000);

        cancelTimer.innerText = `נותרו ${hours} שעות, ${minutes} דקות, ו-${seconds} שניות לשיעור.`;

        // הצגת אזהרה אם נותרו פחות מ-7 שעות
        if (hours > 7) {
            cancelWarning.classList.remove('hidden'); // הצגת ההודעה
        } else {
            cancelWarning.classList.add('hidden'); // הסתרת ההודעה
        }
    }

    // לחיצה על כפתור "סגור" בפופ-אפ ביטול הרשמה
    closeCancelPopup.addEventListener('click', () => {
        clearInterval(cancelInterval); // עצירת הטיימר
        cancelPopup.style.display = 'none';
        overlay.style.display = 'none';
    });

    // לחיצה על כפתור "ביטול ההרשמה שלי"
    confirmCancelBtn.addEventListener('click', () => {
        clearInterval(cancelInterval); // עצירת הטיימר

        const spotsText = selectedSession.querySelector('.spots');
        const current = parseInt(spotsText.textContent.split('/')[0], 10); // מספר הרשומות הנוכחי

        if (current > 0) {
            spotsText.textContent = `${current - 1}/10 רשומות`;
            alert('הרשמתך לשיעור בוטלה בהצלחה!');
        } else {
            alert('לא ניתן לבטל, אינך רשומה לשיעור.');
        }

        cancelPopup.style.display = 'none';
        overlay.style.display = 'none';
    });


// ----סופי----
});

