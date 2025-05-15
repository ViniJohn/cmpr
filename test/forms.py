# forms.py
# forms.py
from django import forms
from .models import Item, Vendor

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'itemflag', 'reportnumber']

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['vendorname', 'value']
        widgets = {
            'vendorname': forms.TextInput(attrs={'class': 'form-control'}),
            'value': forms.NumberInput(attrs={'class': 'form-control'}),
        }

VendorFormSet = forms.inlineformset_factory(
    Item,
    Vendor,
    form=VendorForm,
    extra=0,
    can_delete=True
)

