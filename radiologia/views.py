from datetime import date
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, logout as auth_logout
from .models import *
from validators import FormLoginValidator
from django.contrib.auth.decorators import login_required
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
    tipoid = Tipoid.objects.all()
    tipopaciente = Tipopaciente.objects.all()
    entidad = Entidad.objects.all()
    servicio = Servicio.objects.all()
    docint = Docint.objects.all()
    area = Area.objects.all()
    placa = Tipoconsumible.objects.all()
    hoy = date.today()
    registros = Radiologia.objects.filter(fecha = hoy)
    return render_to_response('radiologia/radiologia.html', {'tipoid':tipoid, 'tipopaciente':tipopaciente, 'entidad':entidad, 'servicio':servicio, 'docint':docint, 'area':area, 'placa':placa, 'registros':registros}, context_instance = RequestContext(request))

@login_required(login_url='/')
def lectura(request):
    return render_to_response('radiologia/lectura.html', context_instance = RequestContext(request))

@login_required(login_url='/')
def consulta_rad(request):
    return render_to_response('radiologia/consulta_rad.html', context_instance = RequestContext(request))

@login_required(login_url='/')
def consulta_eco(request):
    return render_to_response('ecografia/consulta_eco.html', context_instance = RequestContext(request))

@login_required(login_url='/')
def ecografia(request):
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

@login_required(login_url='/')
def especialista(request):
    return render_to_response('ecografia/informe_especialista.html', context_instance = RequestContext(request))

@login_required(login_url='/')
def inventario(request):
    placas = Tipoconsumible.objects.all()
    inventario = Inventario.objects.all()
    return render_to_response('radiologia/inventario.html', {"placas":placas, "inventario":inventario},context_instance = RequestContext(request))

@login_required(login_url='/')
def infoecografia(request):
    return render_to_response('informes/informe_ecografia.html', context_instance = RequestContext(request))

@login_required(login_url='/')
def inforadiologia(request):
    return render_to_response('informes/informe_radiologia.html', context_instance = RequestContext(request))

@login_required(login_url='/')
def usuarios(request):
    return render_to_response('administracion/usuarios.html', context_instance = RequestContext(request))

@login_required(login_url="/")
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect("/")

def registro(request):
    """view del profile
    """
@login_required(login_url='/')
def guardarpersona(request):

    tipoid = Tipoid.objects.all()
    tipopaciente = Tipopaciente.objects.all()

    if request.method == 'POST':
        persona = Persona()
        persona.nombre = request.POST['nombre']
        persona.apellido = request.POST['apellido']
        persona.identificacion = request.POST['identificacion']
        persona.tipoid = Tipoid.objects.get(id = request.POST['tipoid'])
        persona.tipopaciente = Tipopaciente.objects.get(id = request.POST['tipopaciente'])

        persona.save()

        usuario = Persona.objects.get( identificacion = (request.POST['identificacion']))
        output = { 'nombre': usuario.nombre, "apellido": usuario.apellido, "identificacion": usuario.identificacion}

        return HttpResponse(json.dumps(output),  content_type="application/json")

@login_required(login_url='/')
def guardarinventario(request):

    if request.method == 'POST':
        #carga el inventario en la bd
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
def guardarradiologia(request):


    if request.method == 'POST':
        #carga del servicio relacionandolo con el paciente
        spaciente = Serviciopaciente()

        spaciente.servicio = Servicio.objects.get(id = request.POST['servicio'])
        spaciente.persona = Persona.objects.get(identificacion = request.POST['numeroid'])

        spaciente.save()
        #fin de cargue del servicio

        #carga de datos de la tabla principal
        radiologia = Radiologia()

        radiologia.area = Area.objects.get(id = request.POST['area'])
        radiologia.fecha = request.POST['fecha']
        radiologia.hora = request.POST['hora']
        radiologia.entidad = Entidad.objects.get(id = request.POST['entidad'])
        radiologia.serviciopaciente = Serviciopaciente.objects.get(id = spaciente.id)
        radiologia.docint = Docint.objects.get(id = request.POST['docinterno'])
        radiologia.numinterno = request.POST['numinterno']

        if request.POST['insumo'] == '':
            radiologia.cantidadiopamidol = 0.0
        else:
            radiologia.cantidadiopamidol = request.POST['insumo']

        radiologia.tecnico = User.objects.get(id = request.POST['tecnico'])
        radiologia.kilovoltaje = request.POST['kilovoltaje']
        radiologia.miliamperaje = request.POST['miliamperaje']
        radiologia.leido = 0

        radiologia.save()
        #carga de las placas
        placas = Consumibleusado()
        placas.tipoconsumible = Tipoconsumible.objects.get(id = request.POST['placausada'])
        placas.cantidad = request.POST['cantusada']
        placas.radiologia = Radiologia.objects.get(id = radiologia.id)

        placas.save()

        #actualizacion de valores en inventaro
        var = Inventario.objects.get(id = request.POST['placausada'])
        inventario = Inventario(var.id)
        inventario.tipoconsumible = Tipoconsumible.objects.get(id = request.POST['placausada'])
        valorini = var.cantidadsuma
        valorfin = int(request.POST['cantusada'])
        total = valorini - valorfin
        inventario.cantidadsuma = int(total)

        inventario.save()

        return HttpResponseRedirect("/radiologia")

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
def buscar_paciente(request, documento):
    try:
        usuario = Persona.objects.get( identificacion= documento)
        output = { 'nombre': usuario.nombre, "apellido": usuario.apellido}

        return HttpResponse(json.dumps(output),  content_type="application/json")
    except Persona.DoesNotExist:
        output = {'error': 0}
        return HttpResponse(json.dumps(output),  content_type="application/json")
        #return HttpResponse("Usuario no encontrado")

@login_required(login_url='/')
def buscar_servicio(request, codigo):
    try:
        servicio = Servicio.objects.get( codigo = codigo)
        output = { "servicio": servicio.id}
        return HttpResponse(json.dumps(output),  content_type="application/json")
    except Persona.DoesNotExist:
        return HttpResponse("Servicio no encontrado")

@login_required(login_url='/')
def buscar_servicioeco(request, codigo):
    try:
        servicio = Servicioeco.objects.get( codigo = codigo)
        output = { "servicio": servicio.id}
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

