from django import forms
from django.contrib.admin.widgets import AdminDateWidget


class VentaSearchForm(forms.Form):
    numero = forms.CharField(required=False,
                             widget=forms.TextInput(attrs={'placeholder': 'Numero de factura', 'style': 'width:150px;'}))
    cliente = forms.CharField(required=False,
                              widget=forms.TextInput(attrs={'placeholder': 'Cliente', 'style': 'width:220px;'}))
    remision = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Numero de remisión', 'style': 'width:150px;'}))
    desde = forms.DateField(widget=AdminDateWidget(attrs={'placeholder': 'Desde'}), required=False)
    hasta = forms.DateField(widget=AdminDateWidget(attrs={'placeholder': 'Hasta'}), required=False)
