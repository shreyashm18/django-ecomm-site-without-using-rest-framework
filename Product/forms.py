from django import forms
from django.db.models import fields
from .models import Products, Category, Cartitems, Cart

from django.contrib.auth.models import User

class ProductForm(forms.ModelForm):
    class Meta:
        model=Products
        fields='__all__'

class CartItemForm(forms.ModelForm):
    class Meta:
        model=Cartitems
        fields='__all__'

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class SelectCustomer(forms.ModelForm):
    customer = forms.ModelChoiceField(queryset=User.objects.all(),required=True)
    
    class Meta:
        model=User
        fields=['customer',]