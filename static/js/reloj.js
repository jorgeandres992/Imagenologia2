/**
 * Created by andres on 15/05/16.
 */
function mueveReloj() {
    var A = new Date();
    var hora = A.getHours();
    var minuto = A.getMinutes();

    if (hora <= 9)
            hora = "0" + hora
    if (minuto <= 9)
            minuto = "0" + minuto

    var now = hora + ":" + minuto

    $('#hora').val(now);
    setTimeout("mueveReloj()", 1000)
}