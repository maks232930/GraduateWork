from django.urls import path

from .views import (
    PostDetail,
    HomeView,
    reader_view,
    ProfileView,
    PostCreateView,
    PostStatisticsView,
    PostChangeView,
    PostDeleteView,
    about_view,
    message_view,
    delete_message,
    message_detail,
    info_portfolio
)

app_name = 'portfolio'

urlpatterns = [
    path('<str:slug>/', HomeView.as_view(), name='home'),
    path('<str:slug>/about/', about_view, name='about'),
    path('<str:slug>/add-post/', PostCreateView.as_view(), name='add_post'),
    path('<str:slug>/post-management/', PostStatisticsView.as_view(), name='post_statistics'),
    path('<str:slug>/profile/', ProfileView.as_view(), name='profile'),
    path('<str:slug>/readers/', reader_view, name='readers'),
    path('<str:slug>/edit/', info_portfolio, name='edit_portfolio'),
    path('<str:slug>/messages/', message_view, name='messages'),
    path('<str:slug>/messages/delete/<int:pk>/', delete_message, name='delete_message'),
    path('<str:slug>/messages/<int:pk>/', message_detail, name='message_detail'),
    path('<str:slug>/<str:name>/', PostDetail.as_view(), name='post_detail'),
    path('<str:slug>/edit/<str:name>/', PostChangeView.as_view(), name='post_edit'),
    path('<str:slug>/delete/<str:name>/', PostDeleteView.as_view(), name='delete_post'),

]
