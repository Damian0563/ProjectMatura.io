

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

    document.getElementById('signin').addEventListener('click',()=>{
        window.location.href='/logowanie'
    })
    document.getElementById('signup').addEventListener('click',()=>{
        window.location.href='/rejestracja'
    })

    document.getElementById('confirm').addEventListener('click', async()=>{
        const first=document.getElementById('first').value.trim()
        const second=document.getElementById('repeat').value.trim()
        if(first===second && first.trim()!==""){
            try{
                data=await fetch(window.location.href,{
                    method:'PUT',
                    headers:{
                        'Content-Type':'application/json',
                        'X-CSRFToken':csrftoken
                    },
                    body:JSON.stringify({
                        'new_password':first
                    })
                })
                response= await data.json()
                if(response.status===200){
                    document.getElementById('alert').classList.remove('d-none')
                    document.getElementById('alert').classList.add('d-flex')
                    document.getElementById('alert-mess').innerText='Hasło zmienione pomyślnie.✅'
                }
                else{
                    document.getElementById('alert').classList.remove('d-none')
                    document.getElementById('alert').classList.add('d-flex')
                    document.getElementById('alert-mess').innerText='Błąd podczas zmiany hasła.'
                }
            }catch(e){
                console.error(e)
            }
        }else{
            document.getElementById('alert').classList.remove('d-none')
            document.getElementById('alert').classList.add('d-flex')
            document.getElementById('alert-mess').innerText='Podane hasła się różnią. Spróbuj ponownie.'
        }
    })

})