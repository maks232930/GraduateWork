from django.shortcuts import render
from django.views.generic import ListView

from photo_blog_constructor.models import Portfolio


def home_view(request):
    return render(request, 'users/home.html')


class PortfolioListView(ListView):
    model = Portfolio
    context_object_name = 'portfolios'
    template_name = 'users/portfolio_list.html'
