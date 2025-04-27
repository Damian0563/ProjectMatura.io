
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

    document.getElementById('signUP').addEventListener('click',()=>{
        window.location.href='/rejestracja'
    })

    // document.getElementById('sign').addEventListener('click',async()=>{
    //     const mail=document.getElementById('floatingInput').value
    //     const password=document.getElementById('floatingPassword').value
    //     const box=document.getElementById('checkDefault').checked
    //     document.getElementById('floatingInput').value=''
    //     document.getElementById('floatingPassword').value=''
    //     document.getElementById('checkDefault').checked=false
    //     fetch('/logowanie',{
    //         method:"POST",
    //         headers:{
    //             'Content-Type':'application/json',
    //             'X-CSRFToken': csrftoken,
    //         },
    //         credentials:'include',
    //         body:JSON.stringify({
    //             "mail":mail,
    //             "password":password,
    //             "remember":box,
    //         })
    //     })
    //     // .then(response=>response.json())
    //     // .then(data=>{
    //     //     if(data.status==200){
    //     //         window.location.href = data.redirect_url
    //     //     }else if(data.status==404){
    //     //         document.getElementById('message').innerText="Logowanie nie powiodło się.❌"
    //     //         document.getElementById('popup').style.display='grid'
    //     //     }
    //     // })
    //     .catch(e=>console.error(e))
    // })
    

})