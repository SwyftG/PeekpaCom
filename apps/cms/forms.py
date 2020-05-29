from django import forms
from apps.base.forms import FormMixin
from apps.poster.models import Category, Tag, Post
from apps.exchangelink.models import ExchangeLink
from apps.basefunction.models import NavbarItem, FeaturePost
from apps.datacenter.models import Code


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


class PostForm(forms.ModelForm, FormMixin):
    tag_id = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Tag.objects.all(), required=False)

    class Meta:
        model = Post
        exclude = ('tag',)


class PostEditForm(forms.ModelForm, FormMixin):
    tag_id = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Tag.objects.all(),required=False)
    id = forms.CharField(max_length=100)
    class Meta:
        model = Post
        exclude = ('tag',)


class ExchangeLinkForm(forms.ModelForm, FormMixin):
    class Meta:
        model = ExchangeLink
        fields = "__all__"


class ExchangeLinkEditForm(forms.ModelForm, FormMixin):
    pk = forms.CharField(max_length=100)

    class Meta:
        model = ExchangeLink
        fields = "__all__"


class NavItemForm(forms.ModelForm, FormMixin):
    class Meta:
        model = NavbarItem
        fields = "__all__"


class NavItemEditForm(forms.ModelForm, FormMixin):
    pk = forms.CharField(max_length=100)

    class Meta:
        model = NavbarItem
        fields = "__all__"


class CodeForm(forms.ModelForm, FormMixin):
    class Meta:
        model = Code
        exclude = ('visit_num',)


class CodeEditForm(forms.ModelForm, FormMixin):
    pk = forms.CharField(max_length=100)

    class Meta:
        model = Code
        exclude = ('visit_num',)


class UserForm(forms.Form, FormMixin):
    username = forms.CharField(max_length=20)
    email = forms.EmailField()
    password = forms.CharField(max_length=20, min_length=6,
                                error_messages={"max_length": "面最多不能超过20字符", "min_length": "密码最少不得少于6个字符"})


class UserEditForm(forms.ModelForm, FormMixin):
    pk = forms.CharField(max_length=100)

    class Meta:
        model = Code
        exclude = ('visit_num',)


class FeatureForm(forms.ModelForm, FormMixin):
    class Meta:
        model = FeaturePost
        fields = "__all__"


class FeatureEditForm(forms.ModelForm, FormMixin):
    pk = forms.CharField(max_length=100)

    class Meta:
        model = FeaturePost
        fields = "__all__"

