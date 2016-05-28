"""imagenologia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, patterns, include
from django.contrib import admin
from radiologia.views import *

urlpatterns = [
    url(r'^$', login ),
    url(r'^menu$', menu ),
    url(r'^logout$', logout ),
    url(r'^radiologia$', radiologia ),
    url(r'^consulta_rad$', consulta_rad ),
    url(r'^lectura$', lectura ),
    url(r'^ecografia$', ecografia ),
    url(r'^consulta_eco$', consulta_eco ),
    url(r'^especialista$', especialista ),
    url(r'^inventario$', inventario),
    url(r'^infoecografia$', infoecografia ),
    url(r'^inforadiologia$', inforadiologia ),
    url(r'^usuarios$', usuarios ),
    url(r'^entrega_turno$', entrega_turno ),
    url(r'^guardarpersona$', guardarpersona ),
    url(r'^guardarusuario$', guardarusuario ),
    url(r'^guardarradiologia$', guardarradiologia ),
    url(r'^guardarecografia$', guardarecografia ),
    url(r'^guardarinventario$', guardarinventario ),
    url(r'^guardar_lectura$', guardar_lectura ),
    url(r'^guardar_entrega_turno$', guardar_entrega_turno ),
    url(r'^buscarconsultaradiologia$', buscar_consulta_radiologia ),
    url(r'^buscarlectura$', buscar_lectura ),
    url(r'^buscar_entrega_turno$', buscar_entrega_turno ),
    url(r'^reimpresion/$', reimpresion ),
    url(r'^etiquetas/$', etiquetas ),
    url(r'^generar_pdf$', generate_PDF, name= 'Etiqueta' ),
    url(r'^reporte$', reporte ),
    url(r'^buscar/$', buscar_paciente),
    url(r'^buscardoc/(?P<variable>\d+)$', buscar_docint),
    url(r'^searchservice/$', buscar_servicio, name = 'searchservice'),
    url(r'^searchserviceeco/(?P<codigo>\d+)$', buscar_servicioeco),
    url(r'^admin/', admin.site.urls),
]
