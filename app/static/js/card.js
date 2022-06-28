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
    console.log("ok")
    document.querySelector("#nom_local").required = true
    document.querySelector("#direccion").required = true
    document.querySelector("#id_idCategoria").required = true
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
        document.querySelector("#nom_local").required = false
        document.querySelector("#direccion").required = false
        document.querySelector("#id_idCategoria").required = false
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