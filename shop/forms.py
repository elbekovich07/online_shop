from django import forms

from shop.models import Product, Category, Comment


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ()

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'comment']
