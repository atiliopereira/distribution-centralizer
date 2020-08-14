from django import forms
from django.contrib.admin.widgets import AdminDateWidget

from ventas.models import Venta


class VentaSearchForm(forms.Form):
    numero = forms.CharField(required=False,
                             widget=forms.TextInput(attrs={'placeholder': 'Numero de factura', 'style': 'width:150px;'}))
    cliente = forms.CharField(required=False,
                              widget=forms.TextInput(attrs={'placeholder': 'Cliente', 'style': 'width:220px;'}))
    remision = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Numero de remisión', 'style': 'width:150px;'}))
    desde = forms.DateField(widget=AdminDateWidget(attrs={'placeholder': 'Desde'}), required=False)
    hasta = forms.DateField(widget=AdminDateWidget(attrs={'placeholder': 'Hasta'}), required=False)


class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = '__all__'

        widgets = {
            'numero_de_factura': forms.TextInput(attrs={'data-mask': "000-000-0000"}),
            "total": forms.TextInput(
                attrs={'style': 'text-align:right', 'size': '12', 'class': 'auto', 'data-a-sep': '.',
                       'data-a-dec': ','}),
        }

    def __init__(self, *args, **kwargs):
        super(VentaForm, self).__init__(*args, **kwargs)
        self.fields['total'].widget.attrs['readonly'] = True

    def clean(self):
        cleaned_data = super(VentaForm, self).clean()
        total = cleaned_data.get("total")
        if total == 0:
            msg = "Total no puede ser cero."
            self.add_error('total', msg)
