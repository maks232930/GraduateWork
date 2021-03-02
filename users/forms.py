from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.template.defaultfilters import slugify
# from pytils import translit

from photo_blog_constructor.models import Portfolio
from .models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'})
        }


class UserLoginForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(max_length=255, label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(max_length=255, label='Повторите пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name')
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают!!')
        return cd['password2']


class PortfolioForm(forms.ModelForm):
    # name_social_link = forms.ChoiceField(choices=SocialLink.SOCIAL_LINK, widget=forms.Select(attrs={'class':
    # 'form-control'})) social_link = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Portfolio
        fields = ('name', 'user', 'description', 'contact_phone', 'contact_email', 'logo', 'logo_ico',)
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Название дневника', 'class': 'form-control'}),
            'user': forms.HiddenInput(),
            'description': forms.Textarea(attrs={'placeholder': 'Описание', 'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'placeholder': 'Номер телефона', 'class': 'form-control'}),
            'contact_email': forms.TextInput(attrs={'placeholder': 'Email для связи', 'class': 'form-control'}),
        }

    # def save(self, commit=True):
    #     instance = super(PortfolioForm, self).save(commit)
    #     slug = translit.translify(self.cleaned_data['name'])
    #     instance.slug = slugify(slug)
    #     return instance
