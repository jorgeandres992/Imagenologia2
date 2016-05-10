from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Area(models.Model):
    area = models.CharField(max_length=20)
    docint = models.ForeignKey('Docint', models.DO_NOTHING)

    class Meta:
        db_table = 'AREA'

class Docint(models.Model):
    docint = models.CharField(max_length=20)

    class Meta:
        db_table = 'DOCINT'

class Consumibledanado(models.Model):
    tipoconsumible = models.ForeignKey('Tipoconsumible', models.DO_NOTHING)
    cantidad = models.IntegerField(blank=False, null=False)
    radiologia = models.ForeignKey('Radiologia', models.DO_NOTHING)

    class Meta:
        db_table = 'CONSUMIBLEDANADO'

class Consumibleusado(models.Model):
    tipoconsumible = models.ForeignKey('Tipoconsumible', models.DO_NOTHING)
    cantidad = models.IntegerField(blank=False, null=False)
    radiologia = models.ForeignKey('Radiologia', models.DO_NOTHING)

    class Meta:
        db_table = 'CONSUMIBLEUSADO'

class Dosismgy(models.Model):
    id = models.IntegerField(primary_key=True)
    bebe = models.FloatField()
    nino = models.FloatField()
    adulto = models.FloatField()
    adultoobeso = models.FloatField()

    class Meta:
        db_table = 'DOSISMGY'


class Ecografia(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    serviciopacienteeco = models.ForeignKey('Serviciopacienteeco', models.DO_NOTHING)
    entidad = models.ForeignKey('Entidad', models.DO_NOTHING)
    area = models.ForeignKey('Area', models.DO_NOTHING)
    docint = models.ForeignKey('Docint', models.DO_NOTHING)
    numinterno = models.IntegerField(blank=False, null=False)
    usuario = models.ForeignKey(User, models.DO_NOTHING)
    profesional = models.ForeignKey('Profesional', models.DO_NOTHING)

    class Meta:
        db_table = 'ECOGRAFIA'


class Entidad(models.Model):
    entidad = models.CharField(max_length=80)

    class Meta:
        db_table = 'ENTIDAD'


class Entrada(models.Model):
    fechaentrada = models.DateTimeField()
    tipoconsumible = models.ForeignKey('Tipoconsumible', models.DO_NOTHING)
    cantidad = models.IntegerField()
    usuario = models.ForeignKey(User, models.DO_NOTHING)

    class Meta:
        db_table = 'ENTRADA'


class Inventario(models.Model):
    tipoconsumible = models.ForeignKey('Tipoconsumible', models.DO_NOTHING)
    cantidadsuma = models.IntegerField()

    class Meta:
        db_table = 'INVENTARIO'


class Lectura(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    radiologia = models.ForeignKey('Radiologia', models.DO_NOTHING)
    lectura = models.IntegerField()
    observacion = models.TextField(blank=True, null=True)
    profesional = models.ForeignKey('Profesional', models.DO_NOTHING)
    usuario = models.ForeignKey(User, models.DO_NOTHING)

    class Meta:
        db_table = 'LECTURA'

list_sexo = ( ('M', 'Masculino') , ('F', 'Femenino'))
class Persona(models.Model):
    nombre = models.CharField(max_length=60)
    apellido = models.CharField(max_length=60)
    tipoid = models.ForeignKey('Tipoid', models.DO_NOTHING)
    identificacion = models.CharField(max_length=20)
    edad = models.IntegerField()
    genero = models.CharField(max_length=1, choices=list_sexo)
    tipopaciente = models.ForeignKey('Tipopaciente', models.DO_NOTHING)

    class Meta:
        db_table = 'PERSONA'


class Profesional(models.Model):
    profesional = models.CharField(max_length=50)

    class Meta:
        db_table = 'PROFESIONAL'


class Radiologia(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    serviciopaciente = models.ForeignKey('Serviciopaciente', models.DO_NOTHING)
    entidad = models.ForeignKey('Entidad', models.DO_NOTHING)
    area = models.ForeignKey('Area', models.DO_NOTHING)
    docint = models.ForeignKey('Docint', models.DO_NOTHING)
    numinterno = models.IntegerField()
    cantidadiopamidol = models.FloatField(blank=True, null=True)
    kilovoltaje = models.FloatField()
    miliamperaje = models.FloatField()
    tecnico = models.ForeignKey(User, models.DO_NOTHING)
    leido = models.BooleanField(default=0)

    class Meta:
        db_table = 'RADIOLOGIA'

class Servicio(models.Model):
    codigo = models.CharField(max_length=10)
    servicio = models.CharField(max_length=255, blank=True, null=True)
    dosismgy = models.ForeignKey('Dosismgy', models.DO_NOTHING)
    insumo = models.BooleanField(default=0)


    class Meta:
        db_table = 'SERVICIO'


class Servicioeco(models.Model):
    codigo = models.CharField(max_length=10)
    servicio = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'SERVICIOECO'


class Serviciopaciente(models.Model):
    servicio = models.ForeignKey('Servicio', models.DO_NOTHING)
    persona = models.ForeignKey('Persona', models.DO_NOTHING)

    class Meta:
        db_table = 'SERVICIOPACIENTE'


class Serviciopacienteeco(models.Model):
    servicioeco = models.ForeignKey('Servicioeco', models.DO_NOTHING)
    persona = models.ForeignKey('Persona', models.DO_NOTHING)

    class Meta:
        db_table = 'SERVICIOPACIENTEECO'

class Tipoconsumible(models.Model):
    consumible = models.CharField(max_length=8)
    detalle = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'TIPOCONSUMIBLE'


class Tipoid(models.Model):
    tipoid = models.CharField(max_length=2)
    detalle = models.TextField()

    class Meta:
        db_table = 'TIPOID'


class Tipopaciente(models.Model):
    tipopaciente = models.CharField(max_length=20)

    class Meta:
        db_table = 'TIPOPACIENTE'

class Usuario(User):

    class Meta:
        proxy = True