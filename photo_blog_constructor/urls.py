from django.urls import path

from .views import HomeView, PostView

urlpatterns = [
    path('<str:slug>/', HomeView.as_view(), name='home'),
    path('<str:slug>/<str:name>/', PostView.as_view(), name='post_detail')
]
