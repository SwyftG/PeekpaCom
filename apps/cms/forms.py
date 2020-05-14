from django import forms
from apps.base.forms import FormMixin
from apps.poster.models import Category, Tag


class CategoryForm(forms.ModelForm, FormMixin):
    class Meta:
        model = Category
        fields = "__all__"


class CategoryEditForm(forms.ModelForm, FormMixin):
    pk = forms.CharField(max_length=100)

    class Meta:
        model = Category
        fields = "__all__"


class TagForm(forms.ModelForm, FormMixin):
    class Meta:
        model = Tag
        fields = "__all__"


class TagEditForm(forms.ModelForm, FormMixin):
    pk = forms.CharField(max_length=100)

    class Meta:
        model = Tag
        fields = "__all__"