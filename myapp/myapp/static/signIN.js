
document.addEventListener('DOMContentLoaded',()=>{

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

    document.getElementById('forget').addEventListener('click',async()=>{
        const mail=document.getElementById('floatingInput').value
        console.log(mail)
        if(mail!==""){
            try{
                data=await fetch('/encode',{
                    "method":"POST",
                    headers:{
                        'Content-Type':'application/json',
                        'X-CSRFToken':csrftoken
                    },
                    credentials:'include',
                    body:JSON.stringify({
                        'mail':mail
                    })
                })
                response=await data.json()
                if(response.status===200){
                    window.location.href=`${response.url}`
                }else if(response.status===400){
                    document.getElementById('alert').classList.remove('d-none')
                    document.getElementById('alert').classList.add('d-flex')
                    document.getElementById('alert-mess').innerText='Podany adres mailowy nie jest zarejestrowany na naszej platformie. Utwórz konto'
                }
            }catch(e){
                console.error(e)
            }
        }
        else{
            document.getElementById('alert').classList.remove('d-none')
            document.getElementById('alert').classList.add('d-flex')
            document.getElementById('alert-mess').innerText='Wpisz adres mailowy w odpowiednie pole, aby otrzymać formularz odzyskiwania hasła.'
        }
    })
    
    document.getElementById('signUP').addEventListener('click',()=>{
        window.location.href='/rejestracja'
    })

})