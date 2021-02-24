from django.urls import path

from .views import (
    PostDetail,
    HomeView,
    ReaderView,
    ProfileView,
    PostCreateView,
    PostStatisticsView,
    PostChangeView,
    PostDeleteView
)

urlpatterns = [
    path('<str:slug>/', HomeView.as_view(), name='home'),
    path('<str:slug>/add-post/', PostCreateView.as_view(), name='add_post'),
    path('<str:slug>/post-management/', PostStatisticsView.as_view(), name='post_statistics'),
    path('<str:slug>/profile/', ProfileView.as_view(), name='profile'),
    # path('<str:slug>/register/', ReaderView.as_view(), name='register'),
    path('<str:slug>/readers/', ReaderView.as_view(), name='readers'),
    path('<str:slug>/<str:name>/', PostDetail.as_view(), name='post_detail'),
    path('<str:slug>/edit/<str:name>/', PostChangeView.as_view(), name='post_edit'),
    path('<str:slug>/delete/<str:name>/', PostDeleteView.as_view(), name='delete_post'),

]
