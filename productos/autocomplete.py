from dal import autocomplete

from productos.models import Producto


class ProductoAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Producto.objects.exclude(activo=False)
        if self.q:
            qs = qs.filter(descripcion__icontains=self.q)
        return qs
