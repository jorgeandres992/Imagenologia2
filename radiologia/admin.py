from django.contrib import admin

# Register your models here.
from .models import *


class AdminArea(admin.ModelAdmin):
    list_display = ["id", "area"]
    class Meta:
        model = Area

admin.site.register(Area,AdminArea)