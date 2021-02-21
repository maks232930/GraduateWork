from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.views.generic import View

from .forms import ReaderRegistrationForm, PostCreateForm, CommentForm
from .models import Portfolio, Post, Comment, Reader, Photo


class HomeView(View):

    def get(self, request, slug):
        portfolio = Portfolio.objects.get(slug=slug)
        posts = Post.objects.filter(portfolio=portfolio)
        context = {'posts': posts, 'portfolio': portfolio}
        return render(request, 'photo_blog_constructor/index.html', context)


class PostDetail(View):

    def get(self, request, slug, name):
        portfolio = Portfolio.objects.get(slug=slug)
        form = CommentForm()
        post = Post.objects.get(url=name)
        comments = Comment.objects.filter(post=post)
        context = {'post': post, 'portfolio': portfolio, 'comments': comments, 'form': form}
        return render(request, 'photo_blog_constructor/post_detail.html', context)

    def post(self, request, slug, name):
        form = CommentForm(request.POST)
        post = Post.objects.get(url=name)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            reader = Reader.objects.get(user=request.user)
            comment.reader = reader
            comment.save()
            return redirect(post.get_absolute_url())
        return redirect(post.get_absolute_url())


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


class PostCreateView(View):

    def get(self, request, slug):
        portfolio = Portfolio.objects.get(slug=slug)
        if request.user != portfolio.user:
            return redirect('home', slug=slug)
        form = PostCreateForm()
        context = {'portfolio': portfolio, 'form': form}
        return render(request, 'photo_blog_constructor/add-post.html', context)

    def post(self, request, slug):
        portfolio = Portfolio.objects.get(slug=slug)
        if request.user != portfolio.user:
            return redirect('home', slug=slug)
        form = PostCreateForm(request.POST)
        if form.is_valid():
            print('valid')
            post = form.save(commit=False)
            portfolio = Portfolio.objects.get(slug=slug)
            post.portfolio = portfolio
            post.description = form.cleaned_data['description']
            post.home_image = request.FILES['home_image']
            post.save()
            for f in self.request.FILES.getlist('files'):
                data = f.read()
                photo = Photo(post=post)
                photo.file.save(f.name, ContentFile(data))
                photo.save()

            return redirect(post.get_absolute_url())
        print('invalid')
        return redirect('home', slug='keta')
