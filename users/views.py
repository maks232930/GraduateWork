from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import ListView

from photo_blog_constructor.models import Portfolio
from .forms import UserLoginForm, RegistrationForm


def home_view(request):
    return render(request, 'users/home.html')


class PortfolioListView(ListView):
    model = Portfolio
    context_object_name = 'portfolio'
    template_name = 'users/portfolio_list.html'


def login_view(request):
    if request.user.is_authenticated:
        return redirect('users:home')

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('users:home')
            else:
                return redirect('users:login')
    form = UserLoginForm()
    context = {'form': form}
    return render(request, 'users/login.html', context)


def register_view(request):
    if request.user.is_authenticated:
        return redirect('users:home')

    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('users:home')

    context = {'form': form}
    return render(request, 'users/register.html', context)


def user_logout(request):
    logout(request)
    return redirect('users:home')


@login_required
def profile_view(request):
    user = request.user
    portfolio = Portfolio.objects.filter(user=user)
    context = {'portfolio': portfolio}
    return render(request, 'users/profile.html', context)
