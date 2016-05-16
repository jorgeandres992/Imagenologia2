# -*- encoding: utf-8 -*-
from datetime import datetime,date
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.contrib.auth.models import Group
from django.contrib.auth import login as auth_login, logout as auth_logout
from .models import *
from django.contrib.auth.hashers import make_password
from weasyprint import HTML, CSS
from django.template.loader import get_template
from validators import *
import json

# Create your views here.

def login(request):
     if request.method == 'POST':
         validator = FormLoginValidator(request.POST)
         validator.required = ['username','password']

         if validator.is_valid():
            auth_login(request, validator.acceso )
            return HttpResponseRedirect("/menu")
         else:
             return render_to_response('login/login.html', { 'error': validator.getMessage() },  context_instance = RequestContext(request))
     else:
         return render_to_response('login/login.html', context_instance = RequestContext(request))


@login_required(login_url='/')
def menu(request):
     return render(request,'menu/menu.html', context_instance = RequestContext(request))

@login_required(login_url='/')
def radiologia(request):
    if request.user.groups.filter(id = 1).exists() or request.user.groups.filter(id = 2).exists() or request.user.groups.filter(id = 5).exists():
        tipoid = Tipoid.objects.all()
        tipopaciente = Tipopaciente.objects.all()
        entidad = Entidad.objects.all()
        servicio = Servicio.objects.all()
        docint = Docint.objects.all()
        area = Area.objects.all()
        placa = Tipoconsumible.objects.all()
        hoy = date.today()
        registros = Radiologia.objects.filter(fecha = hoy)


        if request.session.has_key('respuesta'):
            ind = 1
            error = request.session.get('respuesta')
            del request.session['respuesta']
        elif request.session.has_key('error'):
            ind = 0
            error = request.session.get('error')
            del request.session['error']
        else:
            ind = 2
            error = "Por favor llene todos los campos de la pantalla"

        return render_to_response('radiologia/radiologia.html', {'ind':ind, 'resp':error, 'tipoid':tipoid, 'tipopaciente':tipopaciente, 'entidad':entidad, 'servicio':servicio, 'docint':docint, 'area':area, 'placa':placa, 'registros':registros}, context_instance = RequestContext(request))
    else:
         return HttpResponseRedirect('/menu')

@login_required(login_url='/')
def lectura(request):
    if request.user.groups.filter(id = 1).exists() or request.user.groups.filter(id = 3).exists() or request.user.groups.filter(id = 5).exists():
        ind = 0
        resp = 'Seleccione el rango de fechas para realizar la consulta'
        if request.session.has_key('lectura'):
            ind = 2
            resp = request.session.get('lectura')
            del request.session['lectura']

        return render_to_response('radiologia/lectura.html',{'ind':ind, 'resp':resp}, context_instance = RequestContext(request))
    else:
         return HttpResponseRedirect('/menu')
@login_required(login_url='/')
def consulta_rad(request):
    if request.user.groups.filter(id = 1).exists() or request.user.groups.filter(id = 2).exists() or request.user.groups.filter(id = 5).exists():
        return render_to_response('radiologia/consulta_rad.html', context_instance = RequestContext(request))
    else:
         return HttpResponseRedirect('/menu')

@login_required(login_url='/')
def consulta_eco(request):
    if request.user.groups.filter(id = 1).exists() or request.user.groups.filter(id = 2).exists() or request.user.groups.filter(id = 5).exists():
        return render_to_response('ecografia/consulta_eco.html', context_instance = RequestContext(request))
    else:
         return HttpResponseRedirect('/menu')

def reporte(request):
    if request.session.has_key('etiqueta'):
        dato = request.session.get('etiqueta')

    if dato['genero'] == 'M':
        genero = 'Masculino'
    elif dato['genero'] == 'F':
        genero = 'Femenino'

    fecha = datetime.strptime(dato['fecha'], "%Y-%m-%d").strftime("%d/%m/%Y")
    return render_to_response('reporte.html', {"nombre":(dato['nombre']+' '+dato['apellido']), 'edad':(dato['edad']), 'genero':genero, 'fecha':fecha,"identificacion":(dato['tipoid'] +'.' + ' '+dato['identificacion']), 'servicio': dato['servicio'], 'tecnico':dato['tecnico']},context_instance = RequestContext(request))


@login_required(login_url='/')
def ecografia(request):
    if request.user.groups.filter(id = 1).exists() or request.user.groups.filter(id = 3).exists() or request.user.groups.filter(id = 5).exists():
        tipoid = Tipoid.objects.all()
        tipopaciente = Tipopaciente.objects.all()
        entidad = Entidad.objects.all()
        servicio = Servicioeco.objects.all()
        docint = Docint.objects.all()
        area = Area.objects.all()
        profesional = Profesional.objects.all()
        hoy = date.today()
        registros = Ecografia.objects.filter(fecha = hoy)

        return render_to_response('ecografia/ecografia.html', {'tipoid':tipoid, 'tipopaciente':tipopaciente, 'entidad':entidad, 'servicio':servicio, 'docint':docint, 'area':area, 'registros':registros, "profesional":profesional}, context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/menu')

@login_required(login_url='/')
def inventario(request):
    if request.user.groups.filter(id = 1).exists() or request.user.groups.filter(id = 2).exists() or request.user.groups.filter(id = 5).exists():
        placas = Tipoconsumible.objects.all()
        inventario = Inventario.objects.all()
        return render_to_response('radiologia/inventario.html', {"placas":placas, "inventario":inventario},context_instance = RequestContext(request))

    else:
         return HttpResponseRedirect('/menu')

@login_required(login_url='/')
def etiquetas(request):
    resp = request.GET['resp']
    if resp == '':
        resp = 'Favor complete los campos para continuar'

    fecha_actual = date.today()
    registros = Radiologia.objects.filter(fecha= fecha_actual)
    return render_to_response('radiologia/reimpresion.html',{'registros':registros, 'resp':resp}, context_instance = RequestContext(request))

@login_required(login_url='/')
def reimpresion(request):
    validator = ValidatorGet(request.GET)
    validator.required = ['consecutivo']

    if validator.is_valid():
        registro  = Radiologia.objects.get(id= request.GET['consecutivo'])
        fecha = str(registro.fecha)
        etiqueta = {'nombre':registro.serviciopaciente.persona.nombre, 'apellido':registro.serviciopaciente.persona.apellido, 'genero':registro.serviciopaciente.persona.genero, 'tipoid':registro.serviciopaciente.persona.tipoid.tipoid, 'identificacion':registro.serviciopaciente.persona.identificacion, 'servicio':registro.serviciopaciente.servicio.servicio,'fecha':fecha, 'tecnico': (registro.tecnico.first_name + ' ' + registro.tecnico.last_name) }

        request.session['etiqueta'] = etiqueta
        return HttpResponseRedirect('/generar_pdf')
    else:
        resp = validator._message
        return HttpResponseRedirect('/etiquetas/?resp='+resp)

@login_required(login_url='/')
def infoecografia(request):
    return render_to_response('informes/informe_ecografia.html', context_instance = RequestContext(request))

@login_required(login_url='/')
def inforadiologia(request):
    return render_to_response('informes/informe_radiologia.html', context_instance = RequestContext(request))

@login_required(login_url='/')
def especialista(request):
    return render_to_response('informes/informe_especialista.html', context_instance = RequestContext(request))

@login_required(login_url='/')
def usuarios(request):
    if request.user.groups.filter(id = 1).exists():
        perfil = Group.objects.all()
        tipoid = Tipoid.objects.all()
        tipopaciente = Tipopaciente.objects.all()
        return render_to_response('administracion/usuarios.html', {'perfil':perfil,'tipoid':tipoid,'tipopaciente':tipopaciente}, context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/menu')

@login_required(login_url="/")
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect("/")

@login_required(login_url="/")
def guardarusuario(request):
    if request.method == 'POST':
        validator = FormRegistroValidator(request.POST)
        validator.required = ['username', 'email','password', 'perfil']

        if validator.is_valid():
            usuario = User()
            persona = Persona.objects.get(identificacion = request.POST['numeroid'])
            usuario.first_name = persona.nombre
            usuario.last_name = persona.apellido
            usuario.username = request.POST['username']
            usuario.email = request.POST['email']
            usuario.password = make_password(request.POST['password'])
            usuario.is_active = True
            perfil = Group.objects.get(id = request.POST['perfil'])
            usuario.save()
            usuario.groups.add( perfil )
            usuario.save()

            resp = 'El usuario ha sido creado exitosamente'
            output = { 'resp': resp, 'indicador': 1 }
            return HttpResponse(json.dumps(output),  content_type="application/json")
        else:
            output = { 'resp': validator.getMessage(), 'indicador':0 }
            return HttpResponse(json.dumps(output),  content_type="application/json")
    else:
        return HttpResponseRedirect('/usuarios')


@login_required(login_url='/')
def guardarpersona(request):
    if request.user.groups.filter(id = 4).exists():
        return HttpResponseRedirect('/menu')
    else:
        if request.method == 'POST':
            if Persona.objects.filter(identificacion= request.POST['identificacion']).exists():
                usuario = Persona.objects.get( identificacion = (request.POST['identificacion']))
                output = { 'nombre': 0, "apellido": 0, "identificacion": usuario.identificacion, 'resp': 'El usuaruo ya existe, favor buscar de nuevo' }
                return HttpResponse(json.dumps(output),  content_type="application/json")
            else:
                validator = Validator(request.POST)
                validator.required = ['nombre', 'apellido','identificacion', 'fechanacimiento', 'genero', 'tipoid']

                if validator.is_valid():
                    persona = Persona()
                    persona.nombre = request.POST['nombre']
                    persona.apellido = request.POST['apellido']
                    persona.identificacion = request.POST['identificacion']
                    persona.fechanacimiento = request.POST['fechanacimiento']
                    persona.genero = request.POST['genero']
                    persona.tipoid = Tipoid.objects.get(id = request.POST['tipoid'])
                    persona.save()

                    usuario = Persona.objects.get( identificacion = (request.POST['identificacion']))
                    output = { 'nombre': usuario.nombre, "apellido": usuario.apellido, "identificacion": usuario.identificacion, 'resp':0 }

                    return HttpResponse(json.dumps(output),  content_type="application/json")
                else:
                    output = { 'resp': validator.getMessage(), 'indicador':0 }
                    return HttpResponse(json.dumps(output),  content_type="application/json")


@login_required(login_url='/')
def guardarinventario(request):
    if request.user.groups.filter(id = 3).exists()or request.user.groups.filter(id = 4).exists():
        return HttpResponseRedirect('/menu')
    else:
        if request.method == 'POST':
            entinventario = Entrada()
            entinventario.fechaentrada = request.POST['fechaentrada']
            entinventario.tipoconsumible = Tipoconsumible.objects.get(id = request.POST['tipoconsumible'])
            entinventario.cantidad = request.POST['cantidad']
            entinventario.usuario = User.objects.get(id = request.POST['usuario'])
            entinventario.save()
            #actualizacion de valores en inventaro
            var = Inventario.objects.get(id = request.POST['tipoconsumible'])
            inventario = Inventario(var.id)
            inventario.tipoconsumible = Tipoconsumible.objects.get(id = request.POST['tipoconsumible'])
            valorini = var.cantidadsuma
            valorfin = int(request.POST['cantidad'])
            total = valorini + valorfin
            inventario.cantidadsuma = int(total)

            inventario.save()

            return HttpResponseRedirect("/inventario")

@login_required(login_url='/')
@transaction.atomic
def guardarradiologia(request):
    if request.user.groups.filter(id = 3).exists() or request.user.groups.filter(id = 4).exists():
        return HttpResponseRedirect('/menu')
    else:
        consum = None
        placas = Inventario.objects.all()
        for p in range(len(placas)):
            if placas[p].cantidadsuma <= 0:
                consum = placas[p].cantidadsuma
                break
        etiqueta = None
        if not consum < 0 or consum is None:
            if request.method == 'POST':
                validator = FormRadiologiaValidator(request.POST)
                validator.required = ['numinterno', 'kilovoltaje', 'miliamperaje', 'cantusada']

                if validator.is_valid():
                    spaciente = cargue_servicio(request)#carga del servicio relacionandolo con el paciente
                    radiologia = Cargue_radiologia(request, spaciente)#carga de datos de la tabla principal
                    placas = request.POST.getlist('placausada')
                    cantidad = request.POST.getlist('cantusada')
                    consumible = Cargue_placas(radiologia, placas,cantidad, request,)#carga de las placas usadas

                    if not request.POST['placadanada'] == '':
                        placas = request.POST.getlist('placadanada')
                        cantidad = request.POST.getlist('cantdanada')
                        consumibled = Cargue_placas(radiologia, placas,cantidad, request,)#carga de las placas danadas
                    tecnico = (radiologia.tecnico.first_name + ' '+radiologia.tecnico.last_name)
                    etiqueta = {'nombre':spaciente.persona.nombre, 'apellido':spaciente.persona.apellido, 'genero':spaciente.persona.genero, 'tipoid':spaciente.persona.tipoid.tipoid, 'identificacion':spaciente.persona.identificacion, 'servicio':spaciente.servicio.servicio,'fecha':radiologia.fecha, 'tecnico': tecnico}

                    request.session['respuesta'] = "El registro ha sido creado exitosamente"
                    request.session['etiqueta'] = etiqueta

                    return HttpResponseRedirect('/radiologia')
                else:
                    request.session['error'] = validator._message

                    return HttpResponseRedirect('/radiologia')
        else:
            aviso = ("La placas del inventario se encuentran agotadas, por favor revise el inventario, EL REGISTRO NO SERA GUARDADO")
            request.session['error'] = aviso
            return HttpResponseRedirect('/radiologia')


def Cargue_placas(radiologia, placas, cantidad, request):
    placas = placas
    cantidad = cantidad
    i = 0
    radiologia = Radiologia.objects.get(id=radiologia.id)
    while i < len(placas):
        consumible = Consumibleusado()
        consumible.tipoconsumible = Tipoconsumible.objects.get(id=placas[i])
        consumible.cantidad = cantidad[i]
        consumible.radiologia = radiologia
        consumible.save()
        var = Inventario.objects.get(tipoconsumible=consumible.tipoconsumible)
        inventario = Inventario(var.id)
        inventario.tipoconsumible = Tipoconsumible.objects.get(id=placas[i])
        valorini = var.cantidadsuma
        valorfin = int(cantidad[i])
        total = valorini - valorfin
        inventario.cantidadsuma = int(total)
        inventario.save()
        i = i + 1
    return consumible


def Cargue_radiologia(request, spaciente):
    radiologia = Radiologia()
    radiologia.area = Area.objects.get(id=request.POST['area'])
    radiologia.tipopaciente = Tipopaciente.objects.get(id=request.POST['tipopaciente'])
    radiologia.fecha = request.POST['fecha']
    radiologia.hora = request.POST['hora']
    radiologia.entidad = Entidad.objects.get(id=request.POST['entidad'])
    radiologia.serviciopaciente = Serviciopaciente.objects.get(id=spaciente.id)
    radiologia.docint = Docint.objects.get(id=request.POST['docinterno'])
    radiologia.numinterno = request.POST['numinterno']

    if request.POST['insumo'] == '':
        radiologia.cantidadiopamidol = 0.0
    elif spaciente.servicio.insumo == 1:
        radiologia.cantidadiopamidol = request.POST['insumo']

    radiologia.tecnico = User.objects.get(id=request.POST['tecnico'])
    radiologia.kilovoltaje = request.POST['kilovoltaje']
    radiologia.miliamperaje = request.POST['miliamperaje']
    radiologia.save()
    return radiologia


def cargue_servicio(request):
    spaciente = Serviciopaciente()
    spaciente.servicio = Servicio.objects.get(id=request.POST['servicio'])
    spaciente.persona = Persona.objects.get(identificacion=request.POST['numeroid'])
    spaciente.save()
    return spaciente


@login_required(login_url='/')
def guardarecografia(request):


    if request.method == 'POST':
        #carga del servicio relacionandolo con el paciente
        spaciente = Serviciopacienteeco()

        spaciente.servicioeco = Servicioeco.objects.get(id = request.POST['servicio'])
        spaciente.persona = Persona.objects.get(identificacion = request.POST['numeroid'])

        spaciente.save()
        #fin de cargue del servicio

        #carga de datos de la tabla principal
        ecografia = Ecografia()

        ecografia.area = Area.objects.get(id = request.POST['area'])
        ecografia.fecha = request.POST['fecha']
        ecografia.hora = request.POST['hora']
        ecografia.entidad = Entidad.objects.get(id = request.POST['entidad'])
        ecografia.serviciopacienteeco = Serviciopacienteeco.objects.get(id = spaciente.id)
        ecografia.docint = Docint.objects.get(id = request.POST['docinterno'])
        ecografia.numinterno = request.POST['numinterno']
        ecografia.usuario = User.objects.get(id = request.POST['usuario'])
        ecografia.profesional = Profesional.objects.get(id = request.POST['profesional'])

        ecografia.save()

        return HttpResponseRedirect("/ecografia")

@login_required(login_url='/')
def guardar_lectura(request):
    if request.method == 'POST':
        ids = request.POST.getlist('id')
        profesional = request.POST.getlist('profesional')
        tecnico = request.POST.getlist('tecnico')
        i = 0
        while i < len(ids):
            lectura = Lectura()
            lectura.fecha = date.today()
            lectura.hora = datetime.now()
            registro = Radiologia.objects.get(id = ids[i])
            lectura.radiologia = registro
            lectura.profesional = Profesional.objects.get(id = profesional[i])
            lectura.usuario = User.objects.get(id=tecnico[i])
            radiologia = Radiologia(registro.id)
            radiologia.fecha =registro.fecha
            radiologia.hora = registro.hora
            radiologia.numinterno = registro.numinterno
            radiologia.cantidadiopamidol = registro.cantidadiopamidol
            radiologia.kilovoltaje = registro.kilovoltaje
            radiologia.miliamperaje = registro.miliamperaje
            radiologia.area = registro.area
            radiologia.docint = registro.docint
            radiologia.entidad = registro.entidad
            radiologia.serviciopaciente = registro.serviciopaciente
            radiologia.tecnico = registro.tecnico
            radiologia.leido = True
            radiologia.save()
            lectura.save()
            i = i + 1

        verificacion_lectura = 'La confirmación de lectura se ha realizado correctamente'
        request.session['lectura'] = verificacion_lectura
        return HttpResponseRedirect("/lectura")


@login_required(login_url='/')
def buscar_paciente(request):
    documento = request.GET['numid']
    try:
        usuario = Persona.objects.get( identificacion= documento)
        output = { 'nombre': usuario.nombre, "apellido": usuario.apellido}

        return HttpResponse(json.dumps(output),  content_type="application/json")
    except Persona.DoesNotExist:
        output = {'error': 0}
        return HttpResponse(json.dumps(output),  content_type="application/json")

@login_required(login_url='/')
def buscar_servicio(request):
    codigo = request.GET['codigo']
    tipo_paciente = request.GET['tipopaciente']

    try:
        if len(codigo) <= 2:
            servicio = Servicio.objects.get( id = codigo)
        elif len(codigo) == 6:
            servicio = Servicio.objects.get( codigo = codigo)
        else:
            servicio = None

        codigoresp = servicio.codigo
        id = servicio.id
        servicios = servicio.servicio
        insumo = servicio.insumo
        print tipo_paciente
        if tipo_paciente == '1':
            dosismgy = servicio.dosismgy.bebe
        elif tipo_paciente == '2':
            dosismgy = servicio.dosismgy.nino
        elif tipo_paciente == '3':
            dosismgy = servicio.dosismgy.adulto
        elif tipo_paciente == '4':
            dosismgy = servicio.dosismgy.adultoobeso
        else:
            dosismgy = 0.0

        output = {'id':id, "servicio": servicios, 'codigo':codigoresp, 'insumo':insumo, 'dosismgy':dosismgy}

        return HttpResponse(json.dumps(output),  content_type="application/json")
    except Servicio.DoesNotExist:
        return HttpResponse("Servicio no encontrado")

@login_required(login_url='/')
def buscar_servicioeco(request, codigo):
    try:
        if len(codigo) <= 2:
            servicio = Servicioeco.objects.get( id = codigo)
        elif len(codigo) == 6:
            servicio = Servicioeco.objects.get( codigo = codigo)
        else:
            servicio = None

        output = { "servicio": servicio.id, 'codigo':servicio.codigo}
        return HttpResponse(json.dumps(output),  content_type="application/json")
    except Persona.DoesNotExist:
        return HttpResponse("Servicio no encontrado")

@login_required(login_url='/')
def buscar_docint(request, variable):
    try:
        docinterno = Area.objects.get( id = variable)
        output = { "docint": docinterno.docint.id}
        return HttpResponse(json.dumps(output),  content_type="application/json")
    except Persona.DoesNotExist:
        return HttpResponse("Docuento interno no encontrado")

@login_required(login_url='/')
def buscar_consulta_radiologia(request):
    registros = Radiologia.objects.filter(fecha__range=(request.POST['fechainicial'],request.POST['fechafinal']))
    indicador = 0
    respuesta = 'Consulta realizada con exito'

    return render_to_response('radiologia/consulta_rad.html', {'indicador':indicador, 'respuesta':respuesta, 'registros':registros}, context_instance = RequestContext(request))
@login_required(login_url='/')
def buscar_lectura(request):

    registros = Radiologia.objects.filter(fecha__range=(request.POST['fechainicial'],request.POST['fechafinal']))
    profesional = Profesional.objects.all()
    ind = 1
    cont = 0
    for i in range(len(registros)):
        if registros[i].leido == False:
            cont = cont + 1

    resp = ('La consulta se ha realizado con exito, se han encontrado '+str(cont)+ ' registros sin confirmación de lectura')

    return render_to_response('radiologia/lectura.html', {'registros':registros,'profesional':profesional,'resp':resp,'ind':ind}, context_instance = RequestContext(request))

@login_required(login_url='/')
def generate_PDF(request):
    dato = None
    if request.session.has_key('etiqueta'):
        dato = request.session.get('etiqueta')
        del request.session['etiqueta']

        if dato['genero'] == 'M':
            genero = 'Masculino'
        elif dato['genero'] == 'F':
            genero = 'Femenino'

        persona = Persona.objects.get(identificacion=dato['identificacion'])
        edad = (date.today().year - persona.fechanacimiento.year) -1
        fecha = datetime.strptime(dato['fecha'], "%Y-%m-%d").strftime("%d/%m/%Y")

        template = get_template("reporte.html")
        context = {"nombre":(dato['nombre']+' '+dato['apellido']), 'edad':edad, 'genero':genero, 'fecha':fecha,"identificacion":(dato['tipoid'] +'.' + ' '+dato['identificacion']), 'servicio': dato['servicio'], 'tecnico':dato['tecnico']}
        html = template.render(RequestContext(request, context))
        response = HttpResponse(content_type='application/pdf')
        HTML(string=html,base_url=request.build_absolute_uri()).write_pdf(response)

        return response
    else:
        return HttpResponse("La etiqueta no ha podido ser generada")