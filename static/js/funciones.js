$(window).ready(function(){
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
        $( "#fecha" ).datepicker();
    });
    $(function(){
         $.ajax("/permiso/" + $("#logueo").val())
             .done(function (data) {
                 var usr = data.permiso;
                 var entrada = usr;
                 if (entrada == 1) {
                     var anuncio = "Bienvenido usuario Administrador, elija una de las siguientes opciones para continuar";
                     $("#rolusr").text(anuncio);
                    }
                 else if (entrada == 2) {
                     var anuncio = "Bienvenido usuario Radiologia, elija una de las siguientes opciones para continuar";
                     $("#rolusr").text(anuncio);
                     $('.ecography').hide();
                     $('.ecograp').hide();
                     $('.manager').hide();
                    }
                 else if(entrada == 3) {
                     var anuncio = "Bienvenido usuario Ecografia, elija una de las siguientes opciones para continuar";
                     $("#rolusr").text(anuncio);
                     $('.radiography').hide();
                     $('.radiolog').hide();
                     $('.manager').hide();
                    }
                 else if(entrada == 4) {
                     var anuncio = "Bienvenido usuario Consultor, elija una de las siguientes opciones para continuar";
                     $("#rolusr").text(anuncio);
                     $('.ecography').hide();
                     $('.radigraphy').hide();
                     $('.consultor').hide();
                     $('.radiology').hide();
                     $('.manager').hide();
                    }
                 else if(entrada == 5) {
                     var anuncio = "Bienvenido usuario Integral, elija una de las siguientes opciones para continuar";
                     $("#rolusr").text(anuncio);
                     $('.manager').hide();
                    }
            })
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

    $("#area").focusout(function() {
        $.ajax("/buscardoc/" + $("#area").val())
                .done(function (data) {
                    var doc_interno = data.docint;
                    $("#docint").val(doc_interno);
                })
                .fail(function () {
                    var error = "Intente colocar el area de nuevo";
                    alert(error);
                    $("#area" ).val('');
                    $("#area" ).focus();
                });
    });


    $("#codservicio").click(function() {
        $.ajax("/searchservice/" + $("#codigo").val())
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
                var nombre_completo = data.nombre + " " + data.apellido;
                var numero_id = data.identificacion;
                $("#nombre").text(nombre_completo);
                $("#numid").val(numero_id);
                $('#nuevoModal').modal('hide');
            }
        });
       return false;

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


function agregarusadas() {
	campo = '<div class="col-xs-12 form-group"> \
				<div class="col-xs-2"> \
					<label class="control-label">Tipo de placa:</label> \
				</div> \
				<div class="col-xs-4"> \
					<select class="form-control" name="placausada[]" required> \
						<option value="">Seleccione</option> \
					</select> \
				</div> \
				<div class="col-xs-2"> \
					<label class="control-label">Cantidad:</label> \
				</div> \
				<div class="col-xs-3"> \
					<input class="form-control" name="cantusada[]" type="interger" required /> \
				</div> \
				<div class="col-xs-1"></div> \
			</div>';
	$("#placas-usadas").append(campo);
}

function agregardanadas() {
	campo = '<div class="col-xs-12 form-group"> \
				<div class="col-xs-2"> \
					<label class="control-label">Tipo de placa:</label> \
				</div> \
				<div class="col-xs-4"> \
					<select class="form-control" name="placadanada[]" > \
						<option value="">Seleccione</option> \
					</select> \
				</div> \
				<div class="col-xs-2"> \
					<label class="control-label">Cantidad:</label> \
				</div> \
				<div class="col-xs-3"> \
					<input class="form-control" name="cantdanada[]" type="interger" /> \
				</div> \
				<div class="col-xs-1"></div> \
			</div>';
	$("#placas-danadas").append(campo);
}