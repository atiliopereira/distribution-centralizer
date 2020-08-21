# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import DetailView

from clientes.models import Cliente, PuntoEntregaCliente
from productos.models import ProductoCliente
from remisiones.models import Remision
from sistema.constants import EstadoDocumento
from ventas.models import Venta


class ClienteDetailView(DetailView):
    model = Cliente
    template_name = "admin/clientes/cliente/cliente_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ClienteDetailView, self).get_context_data(**kwargs)
        context['ventas'] = Venta.objects.filter(cliente=self.object).filter(estado__exact=EstadoDocumento.PENDIENTE).order_by('fecha_de_emision')
        context['puntos'] = PuntoEntregaCliente.objects.filter(cliente=self.object)
        context['remisiones'] = Remision.objects.filter(punto_de_entrega__cliente=self.object).filter(estado__exact=EstadoDocumento.PENDIENTE)
        context['productos'] = ProductoCliente.objects.filter(cliente=self.object)
        return context
