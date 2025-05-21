
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

    document.getElementById('signIN').addEventListener('click',()=>{
        window.location.href='/logowanie'
    })
    
    document.getElementById('create').addEventListener('click',async()=>{
        const mail=document.getElementById('floatingInput').value
        const password=document.getElementById('floatingPassword').value
        let code=""
        for(let i=1;i<=6;i++){
            code+=document.getElementById(i).value
            document.getElementById(i).value=''
        }
        document.getElementById('floatingInput').value=''
        document.getElementById('floatingPassword').value=''
        
        fetch('/rejestracja',{
            method:"POST",
            headers:{'Content-Type':'application/json',
                'X-CSRFToken': csrftoken,
            },
            body:JSON.stringify({
                "mail":mail,
                "password":password,
                "code":code
            })
        }).then(response => response.json())
        .then(data=>{
            if (data.code === "bad") {
                console.log('temp');
            } else {
                window.location.reload();
            }
        })
        .catch(e=>console.error(e))
    })
    document.getElementById('sign').addEventListener('click', async()=>{
        fetch('/check',{
            method:"POST",
            headers:{
                'Content-Type':'application-json',
                'X-CSRFToken': csrftoken,
            },
            body:JSON.stringify({
                "mail":document.getElementById('floatingInput').value
            })
        })
        .then(response=>response.json())
        .then(data=>{
            if(data.code==200){
                document.getElementById('code-form').style.display='block'
            }   
            else if(data.code==400){
                document.getElementById('message').innerText="Rejestracja na podany adres mail się nie powiodła.❌"
                document.getElementById('pop').style.display='flex'
            }
        })
        .catch(e=>console.error(e))
    })
})