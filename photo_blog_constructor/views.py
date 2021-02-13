from django.shortcuts import render
from django.views.generic import View

from .forms import ReaderRegistrationForm
from .models import Portfolio, Post, Comment


class HomeView(View):

    def get(self, request, slug):
        portfolio = Portfolio.objects.get(slug=slug)
        posts = Post.objects.filter(portfolio=portfolio)
        context = {'posts': posts, 'portfolio': portfolio}
        return render(request, 'photo_blog_constructor/index.html', context)


class PostView(View):

    def get(self, request, slug, name):
        portfolio = Portfolio.objects.get(slug=slug)
        post = Post.objects.get(url=name)
        comments = Comment.objects.filter(post=post)
        context = {'post': post, 'portfolio': portfolio, 'comments': comments}
        return render(request, 'photo_blog_constructor/post_detail.html', context)

    # def post(self, request):


class ReaderView(View):

    def get(self, request, slug):
        form = ReaderRegistrationForm()
        portfolio = Portfolio.objects.get(slug=slug)
        context = {'portfolio': portfolio, 'form': form}
        return render(request, 'photo_blog_constructor/register.html', context)
