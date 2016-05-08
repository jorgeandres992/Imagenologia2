from datetime import datetime,date
import weasyprint
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import response
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext, Context
from django.contrib.auth.models import User, Group
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
        return render_to_response('radiologia/lectura.html', context_instance = RequestContext(request))
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
    return render_to_response('reporte.html', context_instance = RequestContext(request))


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
        print validator.getMessage()
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
                persona = Persona()
                persona.nombre = request.POST['nombre']
                persona.apellido = request.POST['apellido']
                persona.identificacion = request.POST['identificacion']
                persona.tipoid = Tipoid.objects.get(id = request.POST['tipoid'])
                persona.tipopaciente = Tipopaciente.objects.get(id = request.POST['tipopaciente'])
                persona.save()

                usuario = Persona.objects.get( identificacion = (request.POST['identificacion']))
                output = { 'nombre': usuario.nombre, "apellido": usuario.apellido, "identificacion": usuario.identificacion, 'resp':0 }

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
        if not consum <= 0 or consum is None:
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

                placas = request.POST.getlist('placausada')
                cantidad = request.POST.getlist('cantusada')
                i = 0
                radiolog = Radiologia.objects.get(id = radiologia.id)

                while i < len(placas):
                    consumible = Consumibleusado()
                    consumible.tipoconsumible = Tipoconsumible.objects.get(id = placas[i])
                    consumible.cantidad = cantidad[i]
                    consumible.radiologia = radiolog
                    consumible.save()
                    var = Inventario.objects.get(tipoconsumible=consumible.tipoconsumible)
                    inventario = Inventario(var.id)
                    inventario.tipoconsumible = Tipoconsumible.objects.get(id = placas[i])
                    valorini = var.cantidadsuma
                    valorfin = int(cantidad[i])
                    total = valorini - valorfin
                    inventario.cantidadsuma = int(total)
                    inventario.save()
                    i = i+1

                print request.POST['placadanada']

                if not request.POST['placadanada'] == '':
                    placasd = request.POST.getlist('placadanada')
                    cantidadd = request.POST.getlist('cantdanada')
                    i = 0
                    radiolog = Radiologia.objects.get(id = radiologia.id)

                    while i < len(placasd):
                        consumibled = Consumibledanado()
                        consumibled.tipoconsumible = Tipoconsumible.objects.get(id = placasd[i])
                        consumibled.cantidad = cantidadd[i]
                        consumibled.radiologia = radiolog
                        consumibled.save()
                        var = Inventario.objects.get(tipoconsumible=consumible.tipoconsumible)
                        inventario = Inventario(var.id)
                        inventario.tipoconsumible = Tipoconsumible.objects.get(id = placasd[i])
                        valorini = var.cantidadsuma
                        valorfin = int(cantidadd[i])
                        total = valorini - valorfin
                        inventario.cantidadsuma = int(total)
                        inventario.save()
                        i = i+1

                tecnico = (radiologia.tecnico.first_name + ' '+radiologia.tecnico.last_name)
                etiqueta = {'nombre':spaciente.persona.nombre, 'apellido':spaciente.persona.apellido, 'tipoid':spaciente.persona.tipoid.tipoid, 'identificacion':spaciente.persona.identificacion, 'servicio':spaciente.servicio.servicio,'fecha':radiologia.fecha, 'tecnico': tecnico}

            request.session['respuesta'] = "El registro ha sido creado exitosamente"
            request.session['etiqueta'] = etiqueta

            return HttpResponseRedirect('/radiologia')
        else:
            aviso = ("La placas del inventario se encuentran agotadas, por favor revise el inventario, EL REGISTRO NO SERA GUARDADO")
            request.session['error'] = aviso
            return HttpResponseRedirect('/radiologia')

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

def buscar_consulta_radiologia(request):
    registros = Radiologia.objects.filter(fecha__range=(request.POST['fechainicial'],request.POST['fechafinal']))
    indicador = 0
    respuesta = 'Consulta realizada con exito'

    return render_to_response('radiologia/consulta_rad.html', {'indicador':indicador, 'respuesta':respuesta, 'registros':registros}, context_instance = RequestContext(request))

def generate_PDF(request):
    dato = None
    if request.session.has_key('etiqueta'):
        dato = request.session.get('etiqueta')
        #del request.session['etiqueta']

    fecha = datetime.strptime(dato['fecha'], "%Y-%m-%d").strftime("%d/%m/%Y")
    template = get_template("reporte.html")
    context = {"nombre":(dato['nombre']+' '+dato['apellido']), 'fecha':fecha,"identificacion":(dato['tipoid'] +'.' + ' '+dato['identificacion']), 'servicio': dato['servicio'], 'tecnico':dato['tecnico']}
    html = template.render(RequestContext(request, context))
    response = HttpResponse(content_type='application/pdf')
    weasyprint.HTML(string=html,base_url=request.build_absolute_uri()).write_pdf(response)
    print fecha
    return response