
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
        document.getElementById('dummy').style.display='none'
        document.getElementById('content').appendChild(div1)
        document.getElementById('content').appendChild(span1)
        document.getElementById('content').appendChild(div2)
        document.getElementById('content').appendChild(span2)
        document.getElementById('content').appendChild(div4)
        document.getElementById('content').appendChild(span4)
        document.getElementById('content').appendChild(div3)
    }
    init()
    document.getElementById('signout').addEventListener('click',async()=>{
        fetch('/main/log_out',{
            method:"POST",
            headers:{
                'Content-Type':'application/json',
                'X-CSRFToken':csrftoken
            },
            credentials:'include',
        })
        .then(response=>{
            console.log(response)
            if(response.ok) window.location.href='/'
        })
        .catch(e=>console.error(e))
    })
    const ids=['Wprowadzenie','Funkcje','LiczbyR','Logarytmy','Równania','Trygonometria','Geometria','Planimetria','Kombinatoryka','Prawdopodobieństwo','Okręgi','Ciągi','ZadaniaO','Podsumowanie']
    const size=ids.length
    ids.forEach(id=>{
        document.getElementById(id).addEventListener('click',()=>{
            for(let i=0;i<size;i++){
                if(ids[i]!=id){
                    document.getElementById(ids[i]).style.opacity=1;
                }
            }
            document.getElementById(id).style.opacity=0.7;
            document.getElementById('content').innerHTML='';
            if(id=="LiczbyR") document.getElementById('head').innerText="Liczby Rzeczywiste";
            else if(id=="ZadaniaO") document.getElementById('head').innerText="Zadania optymalizacyjne";
            else if(id=="Równania") document.getElementById('head').innerText="Równania i nierówności";
            else document.getElementById('head').innerText=id;
            if(document.getElementById(`check${id}`).style.display==='none'){
                document.getElementById('done').style.setProperty("display","flex",'important')
                document.getElementById('done').style.setProperty('innerText','Oznacz jako wykonane','important')
                document.getElementById('dummy').style.setProperty('display','flex','important')
            }else{
                document.getElementById('done').style.setProperty("display","none",'important')
            }
            const div = document.createElement('div');
            div.classList.add("ratio","ratio-16x9","shadow-lg","rounded","overflow-hidden")
            const video = document.createElement('video');
            video.setAttribute('src', `{% static ${id}.avif' %}`);
            video.setAttribute('controls', '');
            video.classList.add("w-100","h-100")
            video.style.objectFit='cover'
            div.appendChild(video);
            document.getElementById('content').appendChild(div);
            if(id!=="Wprowadzenie"){        
                let new_v="";
                if(id=="LiczbyR") new_v="Liczby Rzeczywiste";
                else if(id=="ZadaniaO") new_v="Zadania optymalizacyjne";
                else if(id=="Równania") new_v="Równania i nierówności";
                const down = document.createElement('div');
                const link = document.createElement('a');
                link.setAttribute('href', `static/${new_v}.pdf`);
                link.setAttribute('download', `Zadanie domowe - ${new_v}.pdf`);
                link.textContent = `📄 Pobierz zadanie domowe: ${new_v}`;
                down.className = 'd-flex justify-content-center my-4';
                link.className = 'btn btn-primary';
                document.getElementById('content').appendChild(link);
            }
            document.getElementById('done').addEventListener('click',()=>{
                document.getElementById('done').style.setProperty("display","none",'important')
                document.getElementById(`check${id}`).style.setProperty("display","flex")
                fetch('/progress',{
                    method:"POST",
                    headers:{'Content-Type':'application/json',
                        'X-CSRFToken':csrftoken
                    },
                    body:JSON.stringify({
                        course:id
                    })
                }).catch(e=>console.error(e))
            })
        })
    })




    


})