
document.addEventListener('DOMContentLoaded',()=>{
    const price="price_1RHicrPSN2Tepf6zZ77HkqAZ"
    const stripe=Stripe("pk_test_51QtxlFPSN2Tepf6zdrZnRIC8gWxPOixRz4Wcl0nyfkaneD10XS1l8ryMA96J7k0yagKzWXcKbcn2d2FV0fBwnbok00DSMg3BNm")
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    document.getElementById('buy').addEventListener('click',async()=>{
        const mail=document.getElementById('mail').value
        fetch('/main/create_checkout_session',{
            method:"POST",
            headers:{'Content-Type':'application/json','X-CSRFToken':csrftoken},
            body:JSON.stringify({
                priceId:price,
                mail:mail
            })
        }).then(response=>response.json())
        .then((data) => {
            stripe.redirectToCheckout({sessionId:data.sessionId});
        })

    })

})