import random

from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.template.defaultfilters import slugify
from multiupload.fields import MultiImageField
from pytils import translit

from .models import Comment, Post, Category


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
