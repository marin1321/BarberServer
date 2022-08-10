
const campoChat= document.querySelector(".chat");
const campoEditar= document.querySelector(".campoEditar");
const areaTexto= document.querySelector("textarea");
const msj_campo= document.querySelector(".msj_campo");

/*cambiando el tamano del textarea automaticamente */
areaTexto.addEventListener("keyup", e => {
    areaTexto.style.height= "1.8rem";
    let scHeight= e.target.scrollHeight;
    areaTexto.style.height= `${scHeight}px`;
});


/*Elegir el campo a usar(Chat o editar)*/
let veriEditar= false;
let veriChat= false;
let contadorChat= 0;
let contadorEdit= 0;
let listaId=[];

function Chat(idChat) {
    const btnChat= document.getElementById(`${idChat}`);
    listaId.push(idChat);
    campoChat.style.display= "block";
    veriChat= true;
    veriEditar= false;
    Verificar(++contadorChat);
}

function Editar(idEditar) {
    const btnEditar= document.getElementById(`${idEditar}`);
    listaId.push(idEditar);
    veriEditar= true;
    veriChat= false;
    campoEditar.style.display= "block";
    Verificar(++contadorEdit);
}

// function VerificarChat(contador, boton){

// }

function Verificar(contador){
    const infoAdicional= document.querySelector(".info_adicional");
    let ultimoId= listaId[listaId.length-1];
    let penultimoId= listaId[listaId.length-2];
    infoAdicional.style.display= "none";
    console.log("Editar:",veriEditar,"Chat:", veriChat,"Contador:", contador,"contChat:",contadorChat,"contEdit:",contadorEdit);
    console.log(penultimoId, ultimoId);
    if(penultimoId!=ultimoId && listaId.length>=2){
        let boton= document.getElementById(`${penultimoId}`);
        boton.style.boxShadow="none";
        console.log("Editar:",veriEditar,"Chat:", veriChat,"Contador:", contador,"contChat:",contadorChat,"contEdit:",contadorEdit);
        contadorChat=1;
        contadorEdit=1;
    }
    if(veriChat===true && veriEditar===false){
        let btnChat= document.getElementById(`${ultimoId}`);
        btnChat.style.boxShadow= "0 0 10px 2px #0d6efd inset";
        campoEditar.style.display= "none";
        // btnEditar.style.boxShadow= "none";
        contadorEdit=0;
        console.log("booleanoChat")
        if(contadorChat===2){
            console.log("contadoeChat2")
            campoChat.style.display= "none";
            btnChat.style.boxShadow= "none";
            contadorChat=0;
            infoAdicional.style.display= "block";
        }
    }
    if(veriEditar===true && veriChat===false){
        let btnEditar= document.getElementById(`${ultimoId}`);
        btnEditar.style.boxShadow= "0 0 10px 2px #0d6efd inset";
        campoChat.style.display= "none";
        // btnChat.style.boxShadow= "none";
        contadorChat=0;
        if(contadorEdit===2){
            campoEditar.style.display= "none";
            btnEditar.style.boxShadow= "none";
            contadorEdit=0;
            infoAdicional.style.display= "block";
        }
    }
}