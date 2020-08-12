from django import forms
from django.contrib.admin.widgets import AdminDateWidget


class ProductoClienteSearchForm(forms.Form):
    producto = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Producto', 'style': 'width:120px;'}))
    cliente = forms.CharField(required=False,
                              widget=forms.TextInput(attrs={'placeholder': 'Cliente', 'style': 'width:220px;'}))
    desde = forms.DateField(widget=AdminDateWidget(attrs={'placeholder': 'Desde'}), required=False)
    hasta = forms.DateField(widget=AdminDateWidget(attrs={'placeholder': 'Hasta'}), required=False)
