from django import forms

from shop.models import Product, Comment


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ()


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('product',)
