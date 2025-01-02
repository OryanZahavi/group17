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
        if (days[index] === 'חמישי') {
            button.classList.add('active');
        }
    });
});
