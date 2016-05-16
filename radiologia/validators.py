# -*- encoding: utf-8 -*-
from .models import Usuario
from django.contrib import auth
from django.contrib.auth.models import User


class Validator(object):
    _post  = None
    required = []
    _message = ''

    def __init__(self, post):
        """
        Carga los datos provenientes de un formulario atraves de POST
        @param post: Datos que proviene de POST
        """
        self._post = post

    def is_empty(self, field):
        """
        Verifica si un campo de formulario es vacio
        @param field: nombre del campo de formulario
        """
        if field == '' or field is None:
            return True
        return False

    def is_valid(self):
        """
        Indica si existen errores de formuarlio
        @return Boolean
        """
        # validar campos vacios
        for field in self.required:
            if self.is_empty(self._post[field]):

                self._message = 'El campo %s no puede estar vacio' %  field
                return False

        return True

    def getMessage(self):
        return self._message

class ValidatorGet(object):
    _get  = None
    required = []
    _message = ''

    def __init__(self, get):
        """
        Carga los datos provenientes de un formulario atraves de POST
        @param post: Datos que proviene de POST
        """
        self._get = get

    def is_empty(self, field):
        """
        Verifica si un campo de formulario es vacio
        @param field: nombre del campo de formulario
        """
        if field == '' or field is None:
            return True
        return False

    def is_valid(self):
        """
        Indica si existen errores de formuarlio
        @return Boolean
        """
        # validar campos vacios
        for field in self.required:
            if self.is_empty(self._get[field]):

                self._message = 'El campo %s no puede quedar vacio' %  field
                return False

        return True

    def getMessage(self):
        return self._message

class FormRegistroValidator(Validator):


    def is_valid(self):
        if not super(FormRegistroValidator, self).is_valid():
            return False
        #validar que las contraseñas sehan iguales
        if not self._post['password'] == self._post['rpassword']:
            self._message = 'Las contraseñas no  coinciden'
            return False

        if User.objects.filter(username= self._post['username']).exists():
            self._message = 'El usuario ya existe'
            return False

        if User.objects.filter(email = self._post['email']).exists():
            self._message = 'El correo electrónico ya se encuentra registrado'
            return False
        #Por ultimo retornamos que en caso de que todo marche bien es correcto el formulario
        return True

class FormLoginValidator(Validator):
    acceso = None

    def is_valid(self):
        if not super(FormLoginValidator, self).is_valid():
            return False

        usuario = self._post['username']
        clave = self._post['password']

        self.acceso = auth.authenticate(username = usuario, password = clave )
        if self.acceso is None:
            self._message = 'Usuario o contraseña inválido'
            return False
        return True

class FormRadiologiaValidator(Validator):

    def is_valid(self):
        num =None
        if not super(FormRadiologiaValidator, self).is_valid():
            return False

        while True:
            try:
                num = int(self._post['numinterno'])
                break
            except:
                self._message = 'El número interno ingresado contiene caracteres no validos'
                return False

        while True:
            try:
                num = int(self._post['kilovoltaje'])
                break
            except:
                self._message = 'El kilovoltaje ingresado contiene caracteres no validos'
                return False

        while True:
            try:
                num = float(self._post['miliamperaje'])
                break
            except:
                self._message = 'El miliamperaje ingresado contiene caracteres no validos'
                return False

        while True:
            try:
                num = float(self._post['cantusada'])
                break
            except:
                self._message = 'El campo cantidad placas usadas contiene caracteres no validos'
                return False

        #Por ultimo retornamos que en caso de que todo marche bien es correcto el formulario
        return True