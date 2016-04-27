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
    url('^$', login ),
    url('^menu$', menu ),
    url('^logout$', logout ),
    url('^radiologia$', radiologia ),
    url('^consulta_rad$', consulta_rad ),
    url('^lectura$', lectura ),
    url('^ecografia$', ecografia ),
    url('^consulta_eco$', consulta_eco ),
    url('^especialista$', especialista ),
    url('^inventario$', inventario),
    url('^infoecografia$', infoecografia ),
    url('^inforadiologia$', inforadiologia ),
    url('^usuarios$', usuarios ),
    url('^guardarpersona$', guardarpersona ),
    url('^guardarradiologia$', guardarradiologia ),
    url('^guardarecografia$', guardarecografia ),
    url('^guardarinventario$', guardarinventario ),
    url('^buscar/(?P<documento>\d+)$', buscar_paciente),
    url('^buscardoc/(?P<variable>\d+)$', buscar_docint),
    url('^searchservice/(?P<codigo>\d+)$', buscar_servicio),
    url('^searchserviceeco/(?P<codigo>\d+)$', buscar_servicioeco),
    url(r'^admin/', admin.site.urls),
]
