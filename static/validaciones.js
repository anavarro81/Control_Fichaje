const semana = document.getElementById("dia");

function validarHora() {
    const horas = document.getElementsByClassName("hora");
    horas.forEach(hora => {
        hora.disabled = true;
    });
    return false;
}
