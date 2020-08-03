from django.contrib import admin

from remisiones.models import DetalleDeRemision, Remision


class DetalleDeRemisionInlineAdmin(admin.TabularInline):
    model = DetalleDeRemision
    autocomplete_fields = ('producto', )
    extra = 0


class RemisionAdmin(admin.ModelAdmin):
    inlines = (DetalleDeRemisionInlineAdmin, )
    autocomplete_fields = ('cliente', 'ciudad_de_partida', 'ciudad_de_llegada', 'vehiculo', 'chofer', )
    actions = None


admin.site.register(Remision, RemisionAdmin)
