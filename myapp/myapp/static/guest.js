
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

    document.getElementById('buy1').addEventListener('click',async()=>{
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

    document.getElementById('no').addEventListener('click',()=>{
        document.getElementById('pop').style.display="none"
    })


    document.getElementById('intro').addEventListener('click',()=>{
        document.getElementById('content').innerHTML=''
        document.getElementById('funckje').style.opacity=1
        document.getElementById('intro').style.opacity=0.7
        document.getElementById('head').innerText='Wprowadzenie'
        const div = document.createElement('div');
        div.classList.add("ratio","ratio-16x9","shadow-lg","rounded","overflow-hidden")
        const video = document.createElement('video');
        video.setAttribute('src', "{% static 'introduction.avif' %}");
        video.setAttribute('controls', '');
        video.classList.add("w-100","h-100")
        video.style.objectFit='cover'
        div.appendChild(video);
        document.getElementById('content').appendChild(div);
    })

    document.getElementById('funckje').addEventListener('click',()=>{
        document.getElementById('content').innerHTML=''
        document.getElementById('intro').style.opacity=1;
        document.getElementById('funckje').style.opacity=0.7
        document.getElementById('head').innerText='Funkcje'
        const div = document.createElement('div');
        div.classList.add("ratio","ratio-16x9","shadow-lg","rounded","overflow-hidden")
        const video = document.createElement('video');
        video.setAttribute('src', "{% static 'funkcje.avif' %}");
        video.setAttribute('controls', '');
        video.classList.add("w-100","h-100")
        video.style.objectFit='cover'
        div.appendChild(video);
        document.getElementById('content').appendChild(div);
    })

    function init(){
        document.getElementById('head').innerText="Matura? Nic trudnego!"
        div1=document.createElement('div')
        div1.classList.add("p-3","bg-white","rounded","border","w-50","text-center")
        div1.style.color='black'
        div1.innerText='Dokładnie opracowane zagadnienia'
        span1=document.createElement('span')
        span1.style.fontSize="20px"
        span1.innerHTML="&#8595";

        div2=document.createElement('div')
        div2.classList.add("p-3","bg-white","rounded","border","w-50","text-center")
        div2.style.color='black'
        div2.innerText='Sumienne przygotowanie'
        span2=document.createElement('span')
        span2.style.fontSize="20px"
        span2.innerHTML="&#8595";

        div4=document.createElement('div')
        div4.classList.add("p-3","bg-white","rounded","border","w-50","text-center")
        div4.style.color='black'
        div4.innerText='Przerabianie arkuszy z ubiegłych lat'
        span4=document.createElement('span')
        span4.style.fontSize="20px"
        span4.innerHTML="&#8595";

        div3=document.createElement('div')
        div3.classList.add("p-3","bg-white","rounded","border","w-50","text-center","text-success","fw-semibold")
        div3.innerText='Sukces'

        document.getElementById('content').appendChild(div1)
        document.getElementById('content').appendChild(span1)
        document.getElementById('content').appendChild(div2)
        document.getElementById('content').appendChild(span2)
        document.getElementById('content').appendChild(div4)
        document.getElementById('content').appendChild(span4)
        document.getElementById('content').appendChild(div3)
    }
    init()
})