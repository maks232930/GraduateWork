from django.urls import path

from .views import home_view, PortfolioListView, login_view, user_logout, register_view, profile_view

app_name = 'users'

urlpatterns = [
    path('', home_view, name='home'),
    path('diary/', PortfolioListView.as_view(), name='list_diary'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', user_logout, name='logout'),
    path('profile/', profile_view, name='profile')
]
