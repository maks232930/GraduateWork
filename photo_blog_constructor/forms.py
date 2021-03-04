import random

from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.template.defaultfilters import slugify
from multiupload.fields import MultiImageField
from pytils import translit

from .models import Comment, Post, Contact, Portfolio, Category


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('reader', 'post', 'content')
        readonly_fields = ('date',)

        widgets = {
            'reader': forms.HiddenInput(),
            'post': forms.HiddenInput(),
            'content': forms.Textarea(attrs={'placeholder': 'Комментарий', 'style': 'width:100%'})
        }


class PostForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget(), label='Описание')
    files = MultiImageField(min_num=0, max_num=3, label='Фото 600х300', required=True)

    # category = forms.ModelChoiceField(queryset=Category.objects.filter(portfolio=))

    class Meta:
        model = Post
        fields = (
            'title', 'url', 'home_image', 'portfolio', 'category', 'date', 'views')
        widgets = {
            'portfolio': forms.HiddenInput(),
            'title': forms.TextInput(attrs={'placeholder': 'Заголовок', 'style': 'width:100%'}),
            'url': forms.HiddenInput(),
            'category': forms.Select(),
            'date': forms.DateInput(attrs={'placeholder': 'Фото на главную(300x300)', 'style': 'width:30%'}),
            'views': forms.HiddenInput()

        }

    def save(self, commit=True):
        instance = super(PostForm, self).save(commit)
        url = translit.translify(self.cleaned_data['title'])
        instance.url = f'{random.randint(1, 100000)}-{slugify(url)}'
        return instance


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('portfolio', 'name', 'topic', 'email', 'message')
        widgets = {
            'portfolio': forms.HiddenInput(),
            'name': forms.TextInput(attrs={'placeholder': 'Имя', 'style': 'width:100%'}),
            'topic': forms.TextInput(attrs={'placeholder': 'Тема', 'style': 'width:100%'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'style': 'width:100%'}),
            'message': forms.Textarea(attrs={'placeholder': 'Сообщение', 'style': 'width:100%'}),

        }


class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = (
            'name', 'description', 'contact_phone', 'contact_email', 'logo', 'logo_ico', 'home_color', 'sidebar_color',
            'input_color', 'title_color', 'text_color')
        widgets = {
            'home_color': forms.TextInput(attrs={'type': 'color'}),
            'sidebar_color': forms.TextInput(attrs={'type': 'color'}),
            'input_color': forms.TextInput(attrs={'type': 'color'}),
            'title_color': forms.TextInput(attrs={'type': 'color'}),
            'text_color': forms.TextInput(attrs={'type': 'color'}),
            'name': forms.TextInput(attrs={'placeholder': 'Название дневника', 'style': 'width:100%'}),
            'description': forms.Textarea(attrs={'placeholder': 'Описание', 'style': 'width:100%'}),
            'contact_phone': forms.TextInput(attrs={'placeholder': 'Номер телефона', 'style': 'width:100%'}),
            'contact_email': forms.TextInput(attrs={'placeholder': 'Email для связи', 'style': 'width:100%'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Название категории', 'style': 'width:100%'})
        }

    def save(self, commit=True):
        instance = super(CategoryForm, self).save(commit)
        url = translit.translify(self.cleaned_data['name'])
        instance.slug = slugify(url)
        return instance
