

document.addEventListener('DOMContentLoaded',()=>{

    if(document.getElementById('res')){
        document.getElementById('res').addEventListener('click',()=>{
            document.getElementById('pop').style.display='flex'
        })
    }

    document.getElementById('no').addEventListener('click',()=>{
        document.getElementById('pop').style.display='none'
    })
})