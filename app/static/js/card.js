// let Mostrar = null
// const change1 = () =>{
//     const nuevoForm= document.querySelector(".nuevoForm")
//     const container = document.getElementById('container');
//     container.classList.remove("right-panel-active");
//     nuevoForm.classList.remove("mostrarFormulario");
//     nuevoForm.classList.add("regresarFormulario");
// }
// const change2 = () =>{
//     const container = document.getElementById('container');
//     container.classList.add("right-panel-active");
// }
function Mover(){
    console.log("ok");
    const nuevoForm= document.querySelector(".nuevoForm");
    nuevoForm.classList.add("mostrarFormulario");
    nuevoForm.classList.remove("regresarFormulario");
    const containerForm = document.querySelector(".containerform");
    containerForm.style.marginRight = "20rem";
    Mostrar=true
}

function Regresar(){
    console.log(Mostrar);
    if(Mostrar){
        const nuevoForm= document.querySelector(".nuevoForm")
        nuevoForm.classList.remove("mostrarFormulario");
        nuevoForm.classList.add("regresarFormulario");
        const containerForm= document.querySelector(".containerform");
        containerForm.style.marginRight= "0";
        console.log(containerForm);
        setMostrar(false)
    }else{
        console.log("No esta");
    }
    
}