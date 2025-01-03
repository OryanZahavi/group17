document.addEventListener("DOMContentLoaded", function () {
    const days = ['חמישי', 'רביעי', 'שלישי', 'שני', 'ראשון']; // ימות השבוע בעברית
    const today = new Date(); // תאריך היום הנוכחי
    const currentDay = today.getDay(); // היום הנוכחי בשבוע (0 = ראשון, 6 = שבת)

    // מחשבים את התאריכים של השבוע, ראשון עד חמישי
    const weekDates = [];
    for (let i = 0; i < 5; i++) {
        const date = new Date(today);
        // התאמה כך שראשון הוא התאריך ההתחלתי
        date.setDate(today.getDate() - currentDay + i);
        weekDates.push(date);
    }

    // הופכים את סדר הימים כדי להתאים לסדר מימין לשמאל
    const reversedWeekDates = weekDates.reverse();

    // מעדכן את הכפתורים עם הימים והתאריכים
    const buttons = document.querySelectorAll('.dates button');
    buttons.forEach((button, index) => {
        const formattedDate = reversedWeekDates[index].toLocaleDateString('he-IL', {
            day: '2-digit',
            month: '2-digit',
        });

        button.innerHTML = `${formattedDate}<br>${days[index]}`; // עדכון שם היום והתאריך

        // הדגשה ליום ראשון
        if (days[index] === 'ראשון') {
            button.classList.add('active');
        }
    });

     // --- חלק 2: טיפול ב-popup ---
    const sessions = document.querySelectorAll('.session'); // כל כפתורי השיעורים
    const popups = document.querySelectorAll('.popup'); // כל החלונות
    const closeButtons = document.querySelectorAll('.close-popup'); // כל כפתורי הסגירה
    const overlay = document.querySelector('.overlay'); // ה-overlay


    // הצגת ה-popup כאשר לוחצים על שיעור
    sessions.forEach(session => {
        session.addEventListener('click', () => {
            const popupId = session.getAttribute('data-popup'); // מזהה ה-popup המתאים
            const popup = document.getElementById(popupId);
            if (popup) {
                popup.style.display = 'block'; // הצגת ה-popup
                overlay.style.display = 'block'; // הצגת ה-overlay
            } else {
                console.error(`Popup with ID '${popupId}' not found.`); // הודעת שגיאה אם ה-popup לא נמצא
            }
        });
    });

     // סגירת ה-popup וה-overlay כאשר לוחצים על כפתור "סגור"
    closeButtons.forEach(button => {
        button.addEventListener('click', () => {
            button.parentElement.style.display = 'none'; // הסתרת ה-popup של הכפתור
            overlay.style.display = 'none'; // הסתרת ה-overlay
        });
    });

   // סגירת ה-popup וה-overlay בלחיצה על ה-overlay
    overlay.addEventListener('click', () => {
        const popups = document.querySelectorAll('.popup');
        popups.forEach(popup => {
            popup.style.display = 'none'; // הסתרת כל ה-popupים
        });
        overlay.style.display = 'none'; // הסתרת ה-overlay
    });

});