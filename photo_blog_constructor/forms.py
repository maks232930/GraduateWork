from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.template.defaultfilters import slugify
from multiupload.fields import MultiImageField

from users.models import User
from .models import Comment, Post


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


class ReaderRegistrationForm(forms.ModelForm):
    password = forms.CharField(max_length=255, label='Пароль',
                               widget=forms.PasswordInput(attrs={'placeholder': 'Пароль', 'style': 'width:100%'}))
    password2 = forms.CharField(max_length=255, label='Повторите пароль',
                                widget=forms.PasswordInput(
                                    attrs={'placeholder': 'Повторите пароль', 'style': 'width:100%'}))

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name')
        widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'Email', 'style': 'width:100%'}),
            'username': forms.TextInput(attrs={'placeholder': 'Имя пользователя', 'style': 'width:100%'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Имя', 'style': 'width:100%'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Фамилия', 'style': 'width:100%'}),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают!!')
        return cd['password2']


class PostCreateForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget(), label='Описание')
    files = MultiImageField(min_num=0, max_num=3, label='Фото 600х300', required=False)

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
        instance = super(PostCreateForm, self).save(commit)
        instance.url = slugify(self.cleaned_data['title'])
        return instance
