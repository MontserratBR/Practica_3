from django.contrib import admin

# Register your models here.
from .models import Cliente, Coche, Servicio, CocheServicio

admin.site.register(Cliente)
admin.site.register(Coche)
admin.site.register(Servicio)
admin.site.register(CocheServicio)