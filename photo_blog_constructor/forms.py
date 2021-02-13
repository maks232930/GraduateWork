from django import forms

from users.models import User
from .models import Comment


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
                               widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))
    password2 = forms.CharField(max_length=255, label='Повторите пароль',
                                widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'}))

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name')
        widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'Email'}),
            'username': forms.TextInput(attrs={'placeholder': 'Имя пользователя'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Фамилия'}),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают!!')
        return cd['password2']
