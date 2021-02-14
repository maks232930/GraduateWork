from django.shortcuts import render, redirect
from django.views.generic import View

from .forms import ReaderRegistrationForm, PostForm
from .models import Portfolio, Post, Comment, Reader


class HomeView(View):

    def get(self, request, slug):
        portfolio = Portfolio.objects.get(slug=slug)
        posts = Post.objects.filter(portfolio=portfolio)
        context = {'posts': posts, 'portfolio': portfolio}
        return render(request, 'photo_blog_constructor/index.html', context)


class PostDetail(View):

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

    def post(self, request, slug):
        portfolio = Portfolio.objects.get(slug=slug)
        form = ReaderRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            reader = Reader.objects.create(user=new_user, portfolio=portfolio)
            reader.save()
            return redirect(portfolio.get_absolute_url())
        else:
            form = ReaderRegistrationForm()
            context = {'portfolio': portfolio, 'form': form}
            return render(request, 'photo_blog_constructor/register.html', context)


class ProfileView(View):

    def get(self, request, slug):
        portfolio = Portfolio.objects.get(slug=slug)
        return render(request, 'photo_blog_constructor/profile.html', {'portfolio': portfolio})


class PostView(View):

    def get(self, request, slug):
        portfolio = Portfolio.objects.get(slug=slug)
        form = PostForm()
        context = {'portfolio': portfolio, 'form': form}
        return render(request, 'photo_blog_constructor/add-post.html', context)
