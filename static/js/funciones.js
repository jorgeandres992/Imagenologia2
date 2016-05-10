function comprobar_insumo(data) {
    if (data.insumo == true) {
        $("#insumo").show()
    }
    else {
        $("#insumo").hide()
    }
}

function ajax_buscar_servicio(cod, per) {
    return $.ajax({
        url: "/searchservice/",
        type: 'get',
        data: {codigo: cod, persona: per}
    });
}
$(window).ready(function(){
    $("#insumo").hide()
    $(function() {
        $.datepicker.regional['es'] = {
         closeText: 'Cerrar',
         prevText: '<Ant',
         nextText: 'Sig>',
         currentText: 'Hoy',
         monthNames: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
         monthNamesShort: ['Ene','Feb','Mar','Abr', 'May','Jun','Jul','Ago','Sep', 'Oct','Nov','Dic'],
         dayNames: ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'],
         dayNamesShort: ['Dom','Lun','Mar','Mié','Juv','Vie','Sáb'],
         dayNamesMin: ['Do','Lu','Ma','Mi','Ju','Vi','Sá'],
         weekHeader: 'Sm',
         dateFormat: 'yy-mm-dd',
         firstDay: 1,
         isRTL: false,
         showMonthAfterYear: false,
         yearSuffix: ''
         };
         $.datepicker.setDefaults($.datepicker.regional['es']);
        $( ".fecha" ).datepicker();
    });
    $("#find").click(function() {
        $.ajax("/buscar/" + $("#numid").val())
                .done(function (data) {
                    if (data.error == 0){
                        var error = "El númer ingresado no ha sido encontrado";
                        $("#nombre").text(error);
                        $("#numid" ).focus();
                    }
                    else{
                        var nombre = data.nombre;
                        var apellido = data.apellido;
                        $("#first_name").val(nombre);
                        $("#last_name").val(apellido);
                        $("#nombre").text(data.nombre + ' ' + data.apellido);
                    }
                })
                .fail(function () {
                    var error = "El campo Número de id esta vacio";
                    $("#nombre").text(error);
                    $("#numid" ).focus();
                });
    });

    $("#area").change(function() {
        $.ajax("/buscardoc/" + $("#area").val())
            .done(function (data) {
                var doc_interno = data.docint;
                $("#docint").val(doc_interno);
            })
            .fail(function () {
                $("#docint").val('');
            });
    });

    $("#codservicio").click(function () {
        var cod = $("#codigo").val();
        var per = $("#numid").val();
        ajax_buscar_servicio(cod, per)
            .done(function (data) {
                $("#servicio").val(data.id);
                $("#dosismgy").val(data.dosismgy);
                comprobar_insumo(data);
            })
            .fail(function () {
                alert("El codigo ingresado no existe");
                $( "#codigo" ).val('');
                $( "#servicio" ).val('');
                $( "#codigo" ).focus();
            })
    });
    $("#servicio").change(function () {
        var cod = $("#servicio").val();
        var per = $("#numid").val();
        ajax_buscar_servicio(cod, per)
            .done(function (data) {
                $("#dosismgy").val(data.dosismgy);
                $("#codigo").val(data.codigo);
                comprobar_insumo(data);
            })
            .fail(function () {
                var error = "Error inesperado";
                alert(error);
                $( "#servicio" ).val('');
                $( "#codigo" ).val('');

            });
    });

    $("#codservicioeco").click(function() {
        $.ajax("/searchserviceeco/" + $("#codigo").val())
                .done(function (data) {
                    var servicio_completo = data.servicio;
                    $("#servicio").val(servicio_completo);
                })
                .fail(function () {
                    var error = "El codigo ingresado no existe";
                    alert(error);
                    $( "#codigo" ).val('');
                    $( "#servicio" ).val('');
                    $( "#codigo" ).focus();
                });
    });


    $( "#formguardar" ).on( "submit", function( event ) {
        $.ajax({
            type: 'POST',
            url: 'guardarpersona',
            data: $(this).serialize(),
            success: function(data) {
                if (data.resp == 0){
                    var nombre_completo = data.nombre + " " + data.apellido;
                    var numero_id = data.identificacion;
                    $("#nuevoModal").modal('hide');
                    $("#nombre").text(nombre_completo);
                    $("#numid").val(numero_id);
                }
                else{
                    var error = data.resp;
                    var numero_id = data.identificacion;
                    $("#nuevoModal").modal('hide');
                    $("#nombre").text(error);
                    $("#numid").val(numero_id);
                }
            }
        });
       return false;

   });
    $( "#formusuario" ).on( "submit", function( event ) {
        $.ajax({
            type: 'POST',
            url: 'guardarusuario',
            data: $(this).serialize(),
            success: function(data) {
                if (data.indicador == 1){
                    var aviso = data.resp;
                    $("#avisos").text(aviso);
                    $("#respuesta").removeClass("alert-info");
                    $("#respuesta").addClass("alert-success");
                    $("#respuesta").slideDown(400, function () {
                        $(this).show(3000);
                        $(this).delay(5000).slideUp(800, function () {
                            $(this).hide(3000);
                        });
                    });
                    $('#formusuario').each (function(){this.reset();
                    });
                    $('#nombre').text('');
                    $('#numid').focus;
                }
                else {
                    if (data.indicador == 0) {
                        var aviso = data.resp;
                        $("#avisos").text(aviso);
                        $("#respuesta").removeClass("alert-info");
                        $("#respuesta").addClass("alert-danger");
                        $("#respuesta").slideDown(400, function () {
                            $(this).show(3000);
                            $(this).delay(5000).slideUp(800, function () {
                                $(this).hide(3000);
                            });
                        });
                    }
                }
            }
        });
       return false;
   });
    $("#respuesta").delay(3000).slideUp(500, function () {
            $(this).hide(2000);
    });
    $("#imprimir").click().delay(2000, function(){
        window.open('/generar_pdf', '_blank')
    });
});

$(function() {
    var A = new Date();
    var hora = A.getHours();
    var minuto = A.getMinutes();
    var mes = A.getMonth() + 1;
    var dia = A.getDate();

    if (mes <= 9)
            var month = "0" + mes;
    else
            var month = mes;
    if (dia <= 9)
            var day = "0" + dia;
    else
            var day = dia;
    if (hora <= 9)
            hora = "0" + hora
    if (minuto <= 9)
            minuto = "0" + minuto


    var f_actual =  A.getFullYear() + "-" + month + "-" + day;
    var now = hora + ":" + minuto;

    $('#fecha').val(f_actual);
    $('#hora').val(now);
})
