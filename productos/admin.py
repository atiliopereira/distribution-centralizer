from django.contrib import admin
from django.contrib.admin.decorators import register
from django.utils.safestring import mark_safe

from productos.forms import ProductoClienteSearchForm
from productos.models import Producto, ProductoCliente
from productos.views import get_productoscliente_queryset


@register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    search_fields = ('descripcion',)
    list_display = ('editar', 'ver', 'descripcion', 'precio', 'activo',)
    list_filter = ('activo', )
    actions = None

    def editar(self, obj):
        html = '<a href="/admin/productos/producto/%s" class="icon-block"> <i class="fa fa-edit"></i></a>' % obj.pk
        return mark_safe(html)

    def ver(self, obj):
        html = '<a href="/admin/productos/producto_detail/%s" class="icon-block"> <i class="fa fa-eye"></i></a>' % obj.pk
        return mark_safe(html)


@register(ProductoCliente)
class ProductoClienteAdmin(admin.ModelAdmin):
    search_fields = ('cliente__razon_social', 'producto__descripcion', )
    list_display = ('editar', 'producto', 'cliente', 'precio', 'fecha_de_creacion', )
    autocomplete_fields = ('cliente', 'producto')
    actions = None

    def editar(self, obj):
        html = '<a href="/admin/productos/productocliente/%s" class="icon-block"> <i class="fa fa-edit"></i></a>' % obj.pk
        return mark_safe(html)

    def get_queryset(self, request):
        form = self.advanced_search_form
        qs = get_productoscliente_queryset(request, form)
        return qs

    def changelist_view(self, request, extra_context=None, **kwargs):
        self.my_request_get = request.GET.copy()
        self.advanced_search_form = ProductoClienteSearchForm(request.GET)
        self.advanced_search_form.is_valid()
        self.other_search_fields = {}
        params = request.get_full_path().split('?')

        extra_context = extra_context or {}
        extra_context.update({'asf': ProductoClienteSearchForm,
                              'my_request_get': self.my_request_get,
                              'params': '?%s' % params[1].replace('%2F', '/') if len(params) > 1 else ''
                              })
        request.GET._mutable = True

        for key in self.advanced_search_form.fields.keys():
            try:
                temp = request.GET.pop(key)
            except KeyError:
                pass
            else:
                if temp != ['']:
                    self.other_search_fields[key] = temp
        request.GET_mutable = False

        return super(ProductoClienteAdmin, self) \
            .changelist_view(request, extra_context=extra_context, **kwargs)