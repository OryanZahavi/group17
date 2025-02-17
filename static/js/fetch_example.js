// ############## GET ################
const execute_get_fetch = (e) => {
    e.preventDefault()
    //דרך אחת:
    // const data= fetch('/fetch_example')
    // דרך שנייה:תקח את האאוטפוט ותדפיס אותו  . then זאת מילה שמורה עבור פונקצית fetch
    // res זאת סתם מילה בלי ערך, היא יכולה גם להשתנות
    fetch('fetch_example'
    ).then(
        //מוציא את האובייקט מתוך ה-json
        x => x.json()
    ).then(
        //מוציא את ההודעה מתוך האובייקט
        x => {
            console.log(x.message)
            const title2 = document.querySelector('.title2')
            title2.innerHTML = `The message from BE: ${x.message}`
        }
    ).catch(
        //אם יש טעות אז זה לא ייפול אלה ידפיס err בזכות ה catch
        err => console.error(err)
    )
}

//מייצר מצביע על id= my_form_get שקיים בעצם בדף HTML של fetch_example
const myForm = document.querySelector('#my-form-get');
// המילים אחרות אומר: תהיה בהיכון אם נלחץ הכפתור 'submit' ואם הוא נלחץ אז תעשה את הפונקציה execute_get_fetch
myForm.addEventListener('submit', execute_get_fetch);


// ############## POST ################

const execute_post_fetch = (e) => {
    e.preventDefault()

    const data = {'username': 'Ariel','age':100, 'Interests':['chess','web']}

    fetch('/fetch_example',{
        method: 'POST',
        headers:{'Content-Type': 'application/json'},
        body: JSON.stringify(data)
        // מפה זה כבר אותו הדבר כמו GET
    }).then(
        //מוציא את האובייקט מתוך ה-json
        res => res.json()
    ).then(
        //מוציא את ההודעה מתוך האובייקט
        res => {
            console.log(res)
            const title3 = document.querySelector('.title3')
            title3.innerHTML = `The Login Status: ${res.message}`
        }
    ).catch(
        //אם יש טעות אז זה לא ייפול אלה ידפיס err בזכות ה catch
        err => console.error(err)
    )

}

//מייצר מצביע על id= my_form_get שקיים בעצם בדף HTML של fetch_example
const myFormPost = document.querySelector('#my-form-post');
// המילים אחרות אומר: תהיה בהיכון אם נלחץ הכפתור 'submit' ואם הוא נלחץ אז תעשה את הפונקציה execute_get_fetch
myFormPost.addEventListener('submit', execute_post_fetch);









