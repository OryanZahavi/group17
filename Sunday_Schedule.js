document.addEventListener("DOMContentLoaded", function () {
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
        firstDayOfWeek.setDate(firstDayOfWeek.getDate() - currentDay + 0); // יום ראשון הקרוב
        return firstDayOfWeek;
    }

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
            const formattedDate = weekDates[index].toLocaleDateString('he-IL', {
                day: '2-digit',
                month: '2-digit',
            });

            button.innerHTML = `${formattedDate}<br>${days[index]}`;
            button.dataset.date = weekDates[index].toISOString().split('T')[0]; // שמירת תאריך כ-ID


            // הדגשה ליום ראשון
            if (days[index] === 'ראשון') {
                button.classList.add('active'); // הוספת מחלקה ליום ראשון
            } else {
                button.classList.remove('active'); // הסרת מחלקה מימים אחרים
            }
        });


    }

    // עדכון תאריכים בהתחלה
    updateDates();

    // קישור הפופאפ
    const sessions = document.querySelectorAll('.session');
    const overlay = document.querySelector('.overlay');
    const popup = document.getElementById('popup');
    const popupContent = document.getElementById('popup-content');
    const cancelResultPopup = document.getElementById('cancel-result-popup');
    const finalResultPopup = document.getElementById('final-result-popup');
    const cancelResultMessage = document.getElementById('cancel-result-message');
    const finalCancelBtn = document.getElementById('final-cancel-btn');

    sessions.forEach(session => {
        session.addEventListener('click', () => {
            const popupId = session.getAttribute('data-popup');
            popupContent.textContent = popupId;
            popup.style.display = 'block';
            overlay.style.display = 'block';
        });
    });

    // טיפול בביטול הרשמה
    document.getElementById('cancel-btn').addEventListener('click', () => {
        const sessionId = popupContent.textContent.match(/שעה (\d+:\d+)/)[1];
        const sessionDate = new Date(`2025-01-05T${sessionId}`);
        const now = new Date();
        const hoursUntilSession = (sessionDate - now) / (1000 * 60 * 60);

        if (hoursUntilSession < 7) {
            cancelResultMessage.textContent = "זמן הביטול כבר עבר, אם תבטלי עכשיו תאלצי לשלם.";
        } else {
            const hoursRemaining = Math.floor(hoursUntilSession - 7);
            const minutesRemaining = Math.round((hoursUntilSession - 7 - hoursRemaining) * 60);
            cancelResultMessage.textContent = `נותרו ${hoursRemaining} שעות ו-${minutesRemaining} דקות לביטול השיעור, אחרת תאלצי לשלם.`;
        }

        cancelResultPopup.style.display = 'block';
        popup.style.display = 'none';
    });

    finalCancelBtn.addEventListener('click', () => {
        cancelResultPopup.style.display = 'none';
        finalResultPopup.style.display = 'block';
    });

    overlay.addEventListener('click', () => {
        popup.style.display = 'none';
        cancelResultPopup.style.display = 'none';
        finalResultPopup.style.display = 'none';
        overlay.style.display = 'none';
    });

});

// פופאפים
const sessions = document.querySelectorAll('.session');
const overlay = document.querySelector('.overlay');
const popup = document.getElementById('popup');
const resultPopup = document.getElementById('result-popup');
const popupContent = document.getElementById('popup-content');
const resultMessage = document.getElementById('result-message');

const registerBtn = document.getElementById('register-btn');
const waitlistBtn = document.getElementById('waitlist-btn');
const cancelBtn = document.getElementById('cancel-btn');
const closePopupBtn = document.getElementById('close-popup');


const cancelResultPopup = document.getElementById('cancel-result-popup');
const finalResultPopup = document.getElementById('final-result-popup');
const cancelResultMessage = document.getElementById('cancel-result-message');
const finalCancelBtn = document.getElementById('final-cancel-btn');


// הצגת פופ-אפ עם פרטי שיעור
sessions.forEach(session => {
    session.addEventListener('click', () => {
        const popupId = session.getAttribute('data-popup');
        popupContent.textContent = `${popupId}`;
        popup.style.display = 'block';
        overlay.style.display = 'block';
    });
});


// לחיצה על "הרשמה"
registerBtn.addEventListener('click', () => {
    resultMessage.textContent = "הרשמתך לשיעור בוצעה בהצלחה!";
    popup.style.display = 'none';
    resultPopup.style.display = 'block';
    overlay.style.display = 'block';

});

// לחיצה על "רשימת המתנה"
waitlistBtn.addEventListener('click', () => {
    resultMessage.textContent = "נכנסת לרשימת המתנה!";
    popup.style.display = 'none';
    resultPopup.style.display = 'block';
    overlay.style.display = 'block';

});

// לחיצה על "סגור"
closePopupBtn.addEventListener('click', () => {
    popup.style.display = 'none';
    overlay.style.display = 'none';
});


// סגירת כל חלון בלחיצה על ה-overlay
overlay.addEventListener('click', () => {
    popup.style.display = 'none';
    cancelResultPopup.style.display = 'none';
    finalResultPopup.style.display = 'none';
    resultPopup.style.display = 'none';
    overlay.style.display = 'none';
});

//-------------------

// טיפול בביטול הרשמה
cancelBtn.addEventListener('click', () => {
    const sessionId = popupContent.textContent.match(/שעה (\d+:\d+)/)[1]; // חילוץ השעה מהתוכן
    const sessionDate = new Date(`2025-01-05T${sessionId}`); // תאריך ושעה של השיעור
    const now = new Date();
    const hoursUntilSession = (sessionDate - now) / (1000 * 60 * 60);

    if (hoursUntilSession < 7) {
        cancelResultMessage.textContent = "זמן הביטול כבר עבר, אם תבטלי עכשיו תאלצי לשלם.";
        document.getElementById('final-cancel-btn').classList.remove('hidden'); // מאפשר ביטול סופי
    } else {
        const hoursRemaining = Math.floor(hoursUntilSession - 7);
        const minutesRemaining = Math.round((hoursUntilSession - 7 - hoursRemaining) * 60);
        cancelResultMessage.textContent = `נותרו ${hoursRemaining} שעות ו-${minutesRemaining} דקות לביטול השיעור, אחרת תאלצי לשלם.`;
        document.getElementById('final-cancel-btn').classList.remove('hidden'); // מאפשר ביטול סופי
    }
    cancelResultPopup.style.display = 'block';
    popup.style.display = 'none';
});

// טיפול בכפתור "ביטול שיעור" הסופי
finalCancelBtn.addEventListener('click', () => {
    cancelResultPopup.style.display = 'none';
    finalResultPopup.style.display = 'block';


});
