from django.shortcuts import render
from django.views.generic import View

from .models import Portfolio, Post


class HomeView(View):

    def get(self, request, slug):
        portfolio = Portfolio.objects.get(slug=slug)
        posts = Post.objects.filter(portfolio=portfolio)
        context = {'posts': posts, 'portfolio': portfolio}
        return render(request, 'photo_blog_constructor/index.html', context)


class PostView(View):

    def get(self, request, slug, name):
        portfolio = Portfolio.objects.get(slug=slug)
        post = Post.objects.get(name=name)
        context = {'posts': post, 'portfolio': portfolio}
        return render(request, 'photo_blog_constructor/post_detail.html', context)
