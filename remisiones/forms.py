from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import AdminDateWidget, AutocompleteSelect

from remisiones.models import Remision
from sistema.constants import EstadoDocumento


class RemisionSearchForm(forms.Form):
    numero = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Numero', 'style': 'width:120px;'}))
    cliente = forms.CharField(required=False,
                              widget=forms.TextInput(attrs={'placeholder': 'Cliente', 'style': 'width:220px;'}))
    punto_de_entrega = forms.CharField(required=False,
                              widget=forms.TextInput(attrs={'placeholder': 'Punto de entrega', 'style': 'width:250px;'}))
    desde = forms.DateField(widget=AdminDateWidget(attrs={'placeholder': 'Desde'}), required=False)
    hasta = forms.DateField(widget=AdminDateWidget(attrs={'placeholder': 'Hasta'}), required=False)


class RemisionForm(forms.ModelForm):
    class Meta:
        model = Remision
        fields = '__all__'

        widgets = {
            'punto_de_entrega': AutocompleteSelect(
                Remision._meta.get_field('punto_de_entrega').remote_field,
                admin.site,
                attrs={'data-dropdown-auto-width': 'true', 'style': "width: 100%;"}
            ),
        }

    def clean(self):
        cleaned_data = super(RemisionForm, self).clean()
        numero_de_remision = cleaned_data.get("numero_de_remision")

        if Remision.objects.filter(numero_de_remision=numero_de_remision,
                                   estado=EstadoDocumento.PENDIENTE).exists() or Remision.objects.filter(
                numero_de_remision=numero_de_remision, estado=EstadoDocumento.CONFIRMADO).exists():
            msg = "Ya existe una remisión con ese número."
            self.add_error('numero_de_remision', msg)