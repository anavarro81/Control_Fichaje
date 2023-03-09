Date.prototype.getWeek = function () {
    var onejan = new Date(this.getFullYear(), 0, 1);
    var today = new Date(this.getFullYear(), this.getMonth(), this.getDate());
    var dayOfYear = ((today - onejan + 86400000) / 86400000);
    return Math.ceil(dayOfYear / 7)
};

document.addEventListener("DOMContentLoaded", function () {

    // Obtener la tabla y las filas
    var tabla = document.querySelector("table");
    var filas = tabla.querySelectorAll("tr");

    // Obtener la semana actual
    var fechaActual = new Date();

    // Obtener el año y número de semana de la fecha actual
    var year = fechaActual.getFullYear();
    var week = fechaActual.getWeek();

    // Construir la cadena de la semana actual en formato 'YYYY-WW'
    var semanaActual = year + '-W' + week;
    var semana = document.querySelector('input[type = "week"]');
    semana.max = semanaActual;

    semana.addEventListener("change", function () {
        console.log("semana", semana.value);
        console.log("semanaghghghg", typeof semana.value);
    });

    // Seleccionar todos los campos de hora
    var camposHora = document.querySelectorAll(".hora");

    // Agregar evento onchange a cada campo de hora
    camposHora.forEach(function (campo) {
        campo.addEventListener("change", function () {
            // Obtener la fila a la que pertenece el campo de hora cambiado
            var fila = this.parentNode.parentNode;

            // Obtener los valores de las horas de entrada y salida de la fila
            var horaEntrada = fila.querySelector(".hora[name='hr_entrada']").value;
            var horaSalida = fila.querySelector(".hora[name='hr_salida']").value;

            // Calcular la diferencia de tiempo entre las dos horas
            var tiempoTranscurrido = calcularTiempo(horaEntrada, horaSalida);

            console.log('tiempoTranscurrido', tiempoTranscurrido);

            // Mostrar la diferencia de tiempo en la columna correspondiente
            fila.querySelector("td:nth-child(4)").textContent = tiempoTranscurrido;
        });
    });


    // Función para calcular la diferencia de tiempo entre dos horas
    function calcularTiempo(hora1, hora2) {
        var fecha1 = new Date("2000-01-01T" + hora1 + ":00Z");
        var fecha2 = new Date("2000-01-01T" + hora2 + ":00Z");

        var diferencia = Math.abs(fecha2 - fecha1) / 1000;
        var horas = Math.floor(diferencia / 3600);
        var minutos = Math.floor((diferencia % 3600) / 60);

        return horas.toString().padStart(2, "0") + ":" + minutos.toString().padStart(2, "0");
    }


});