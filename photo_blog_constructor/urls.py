from django.urls import path

from .views import PostDetail, HomeView, ReaderView, ProfileView, PostCreateView

urlpatterns = [
    path('<str:slug>/', HomeView.as_view(), name='home'),
    path('<str:slug>/add-post/', PostCreateView.as_view(), name='add_post'),
    path('<str:slug>/profile/', ProfileView.as_view(), name='profile'),
    path('<str:slug>/register/', ReaderView.as_view(), name='register'),
    path('<str:slug>/<str:name>/', PostDetail.as_view(), name='post_detail'),

]
