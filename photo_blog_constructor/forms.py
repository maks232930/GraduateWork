from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from multiupload.fields import MultiImageField

from users.models import User
from .models import Comment, Post, Photo


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('reader', 'post', 'content')
        readonly_fields = ('date',)

        widgets = {
            'reader': forms.HiddenInput(),
            'post': forms.HiddenInput()
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
    description = forms.CharField(widget=CKEditorUploadingWidget())
    files = MultiImageField(min_num=1, max_num=3)

    class Meta:
        model = Post
        fields = (
            'title', 'url', 'home_image', 'portfolio', 'category', 'client', 'budget', 'date')

    def save(self, commit=True):
        instance = super(PostCreateForm, self).save(commit)
        for each in self.cleaned_data['files']:
            Photo.objects.create(file=each, post=instance)

        return instance
