# forms.py
from django import forms
from .models import ProductCategory, Realisation, DevisDemande, ContactMessage, ProductInfo

class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = '__all__'

class ProductInfoForm(forms.ModelForm):
    class Meta:
        model = ProductInfo
        fields = '__all__'

class RealisationForm(forms.ModelForm):
    class Meta:
        model = Realisation
        fields = '__all__'

class DevisDemandeForm(forms.ModelForm):
    class Meta:
        model = DevisDemande
        fields = '__all__'

class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = '__all__'

