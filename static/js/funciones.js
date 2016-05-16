function ajax_buscar_servicio(codigo, tipopaciente) {
    return $.ajax({
        url: "/searchservice/",
        type: 'get',
        data: {codigo: codigo, tipopaciente: tipopaciente}
    });
}

function verificacion_campos_requeridos(tipopaciente, codigo) {
    if (tipopaciente == "") {
        swal({
            title: "Faltan campos",
            text: "El campo Tipo paciente se encuentra vacio",
            type: "error"
        });
        $("#servicio").val('');
        $("#codigo").val('');
        $("#tipopaciente").focus();
        return 0
    }
    else if (codigo == "") {
        swal({
            title: "Faltan campos",
            text: "El campo codigo se encuentra vacio",
            type: "error"
        });
        $("#servicio").val('');
        $("#codigo").val('');
        $("#codigo").focus();
        return 0
    }
    else {
        return 1
    }
}
$(window).ready(function(){
    $("#insumo").hide();
    $("#find").click(function() {
        $.ajax({
                url: "/buscar/",
                type: 'get',
                data: {numid: $("#numid").val()}
            })
            .done(function (data) {
                if (data.error == 0) {
                    var error = "El númer ingresado no ha sido encontrado";
                    $("#nombres").text(error);
                    $("#numid").focus();
                }
                else {
                    var nombre = data.nombre;
                    var apellido = data.apellido;
                    $("#first_name").val(nombre);
                    $("#last_name").val(apellido);
                    $("#nombres").text(data.nombre + ' ' + data.apellido);
                }
            })
            .fail(function () {
                var error = "El campo Número de id esta vacio";
                $("#nombre").text(error);
                $("#numid").focus();
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
        var codigo = $("#codigo").val();
        var tipopaciente = $("#tipopaciente").val();

        if (verificacion_campos_requeridos(tipopaciente, codigo) == 1){
            ajax_buscar_servicio(codigo, tipopaciente)
                .done(function (data) {
                    $("#servicio").val(data.id);
                    $("#dosismgy").val(data.dosismgy);
                    if (data.insumo == true) {
                        $("#insumo").show()
                    }
                    else {
                        $("#insumo").hide()
                    }
                })
                .fail(function () {
                    swal({
                        title: "Error",
                        text: "El codigo ingresado no existe",
                        type: "error"
                    });
                    $("#codigo").val('');
                    $("#servicio").val('');
                    $("#codigo").focus();
                    $("#insumo").hide()
                })
        }

    });
    $("#servicio").change(function () {
        var codigo = $("#servicio").val();
        var tipopaciente = $("#tipopaciente").val();

        if (verificacion_campos_requeridos(tipopaciente, codigo) == 1) {

            ajax_buscar_servicio(codigo, tipopaciente)
                .done(function (data) {
                    $("#dosismgy").val(data.dosismgy);
                    $("#codigo").val(data.codigo);
                    if (data.insumo == true) {
                        $("#insumo").show()
                    }
                    else {
                        $("#insumo").hide()
                    }
                })
                .fail(function () {
                    var error = "Favor seleccione el tipo de paciente primero ";
                    alert(error);
                    $("#servicio").val('');
                    $("#codigo").val('');
                    $("#insumo").hide();
                });
        };
    });

    $("#codservicioeco").click(function() {
        $.ajax("/searchserviceeco/" + $("#codigo").val())
            .done(function (data) {
                var servicio_completo = data.servicio;
                $("#servicioeco").val(servicio_completo);
            })
            .fail(function () {
                var error = "El codigo ingresado no existe";
                alert(error);
                $( "#codigo" ).val('');
                $( "#servicioeco" ).val('');
                $( "#codigo" ).focus();
            });
    });
    $("#servicioeco").change(function() {
        $.ajax("/searchserviceeco/" + $("#servicioeco").val())
            .done(function (data) {
                $("#codigo").val(data.codigo);
            })
            .fail(function () {
                var error = "El codigo ingresado no existe";
                alert(error);
                $( "#codigo" ).val('');
                $( "#servicioeco" ).val('');
                $( "#servicioeco" ).focus();
            });
    });


    $( "#formguardar" ).on( "submit", function( event ) {
        $.ajax({
            type: 'POST',
            url: 'guardarpersona',
            data: $(this).serialize(),
            success: function (data) {
                if (data.resp == 0) {
                    var nombre_completo = data.nombre + " " + data.apellido;
                    var numero_id = data.identificacion;
                    $("#nuevoModal").modal('hide');
                    $("#nombres").text(nombre_completo);
                    $("#numid").val(numero_id);
                }
                else {
                    var error = data.resp;
                    var numero_id = data.identificacion;
                    $("#nuevoModal").modal('hide');
                    $("#nombres").text(error);
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
    $("#respuesta_lectura").delay(5000).slideUp(500, function () {
            $(this).hide(3000);
    });
    $('#imprimir').click(function(){
        $("#resp-success").hide()
    });
    $('#button').click( function(){
        if ($('#consecutivo').val() == ''){
            swal({
                title: "Faltan campos",
                text: "El campo no puede quedar vacio",
                type: "error"
            });

            $('#consecutivo').focus()
        }
        else {
            window.open('/reimpresion/?consecutivo=' + $('#consecutivo').val(), '_blank');
        }
    });
    $('#nombre').valid_keypress(' abcdefghijklmnñopqrstuvwxyzáéiou');
    $('#apellido').valid_keypress(' abcdefghijklmnñopqrstuvwxyzáéiou');
    $('#numinterno').valid_keypress('0123456789');
    $('#identificacion').valid_keypress('0123456789');
    $('#kilovoltaje').valid_keypress('0123456789.');
    $('#miliamperaje').valid_keypress('0123456789.');
    $('#guardar_persona').mouseenter(function(){
        if ($("#genero").prop('checked') || $("#genero1").prop('checked')){

        }
        else{
            swal({
                title: "Faltan campos",
                text: "Favor seleccione el genero de la persona",
                type: "error"
            });
        }
    });
    $('#guardar').mouseenter(function(){
        if ($('.placausada').val() == ''){
            swal({
                title: "Faltan campos",
                text: "Favor registre las placas usadas en el estudio",
                type: "error"
            });
            $('#placausada_btn').click();
        }
        else {
            if($('.cantusada').val() == '' || $('.cantusada').val() == '0'){
                swal({
                    title: "Faltan campos",
                    text: "Favor registre la cantidad de placas usadas en el estudio",
                    type: "error"
                    });
                $('#placausada_btn').click();
            }
        }
    });

});

$(function() {
    var A = new Date();
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

    var f_actual =  A.getFullYear() + "-" + month + "-" + day;

    $('#fecha').val(f_actual);
})

