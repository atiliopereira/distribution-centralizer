from django.contrib import admin
from django.contrib.admin import register

from sistema.models import Ciudad, Vehiculo, Cargo, Funcionario, UnidadDeMedida, Departamento, Local


@register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', )
    ordering = ('nombre', )
    search_fields = ('nombre', )
    actions = None


@register(Ciudad)
class CiudadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'departamento',)
    ordering = ('nombre', )
    search_fields = ('nombre', )
    list_filter = ('departamento', )
    actions = None


@register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('rua', 'rua_remolque', 'marca')
    search_fields = ('rua', 'rua_remolque',)
    list_filter = ('marca', )
    actions = None


@register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ('descripcion', )
    search_fields = ('descripcion', )
    actions = None


@register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cargo', 'ruc', 'direccion', 'email', 'fecha_de_ingreso', 'usuario')
    search_fields = ('nombre', 'ruc', 'direccion', 'email', 'usuario')
    list_filter = ('cargo', )
    actions = None


@register(UnidadDeMedida)
class UnidadDeMedidaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'simbolo')
    search_fields = ('nombre', )
    actions = None


@register(Local)
class LocalAdmin(admin.ModelAdmin):
    list_display = ('referencia', 'direccion', 'ciudad', )
    search_fields = ('referencia', 'direccion', )
    list_filter = ('ciudad', 'ciudad__departamento')
    actions = None