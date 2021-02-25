from django.urls import path

from .views import home_view, PortfolioListView


urlpatterns = [
    path('', home_view),
    path('diary/', PortfolioListView.as_view(), name='list_diary')
]
