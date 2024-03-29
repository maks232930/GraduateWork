from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.db.models import F
from django.shortcuts import render, redirect
from django.views.generic import View

from .forms import PostForm, CommentForm, ContactForm, PortfolioForm, CategoryForm
from .models import Portfolio, Post, Comment, Reader, Photo, Contact, Like
from .utils import is_reader, ReaderMixin


class HomeView(View, ReaderMixin):
    def get(self, request, slug):
        if self.is_reader(request=request, slug=slug):
            portfolio = Portfolio.objects.get(slug=slug)
            posts = Post.objects.filter(portfolio=portfolio)
            context = {'posts': posts, 'portfolio': portfolio}
            return render(request, 'photo_blog_constructor/index.html', context)
        return redirect('users:home')


class PostDetail(View, ReaderMixin):
    def get(self, request, slug, name):
        if self.is_reader(request=request, slug=slug):
            portfolio = Portfolio.objects.get(slug=slug)
            form = CommentForm()
            post = Post.objects.get(url=name)
            comments = Comment.objects.filter(post=post)
            post.views = F('views') + 1
            post.save()
            if request.GET.get('like'):
                reader = Reader.objects.get(user=request.user, portfolio=post.portfolio)
                if not Like.objects.filter(post=post, reader=reader):
                    like = Like.objects.create(post=post, reader=reader)
                    like.save()
            context = {'post': post, 'portfolio': portfolio, 'comments': comments, 'form': form}
            return render(request, 'photo_blog_constructor/post_detail.html', context)
        return redirect('users:home')

    def post(self, request, slug, name):
        if self.is_reader(request=request, slug=slug):
            form = CommentForm(request.POST)
            post = Post.objects.get(url=name)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                reader = Reader.objects.get(user=request.user, portfolio=post.portfolio)
                comment.reader = reader
                comment.save()
                return redirect(post.get_absolute_url())
            return redirect(post.get_absolute_url())
        return redirect('users:home')


class PostCreateView(View):

    def get(self, request, slug):
        portfolio = Portfolio.objects.get(slug=slug)
        if request.user != portfolio.user:
            return redirect('home', slug=slug)
        form = PostForm()
        context = {'portfolio': portfolio, 'form': form}
        return render(request, 'photo_blog_constructor/add-post.html', context)

    def post(self, request, slug):
        portfolio = Portfolio.objects.get(slug=slug)
        if request.user != portfolio.user:
            return redirect('home', slug=slug)
        form = PostForm(request.POST)
        form.errors.clear()
        if form.is_valid():
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
        messages.error(request, 'Проверьте поля')
        return redirect('add_post', slug=portfolio.slug)


class PostStatisticsView(View):

    def get(self, request, slug):
        user = request.user
        portfolio = Portfolio.objects.get(slug=slug)
        if portfolio.user != user:
            return redirect('home', slug=slug)
        posts = Post.objects.filter(portfolio=portfolio)
        context = {'portfolio': portfolio, 'posts': posts}
        return render(request, 'photo_blog_constructor/post_statistics.html', context)


class PostChangeView(View):

    def get(self, request, slug, name):
        user = request.user
        portfolio = Portfolio.objects.get(slug=slug)
        if portfolio.user != user:
            return redirect('home', slug=slug)
        post = Post.objects.get(url=name)
        files = Photo.objects.filter(post=post)
        form = PostForm(instance=post, initial={'description': post.description, 'files': files})
        context = {'portfolio': portfolio, 'form': form, 'post': post}
        return render(request, 'photo_blog_constructor/edit_post.html', context)

    def post(self, request, slug, name):
        user = request.user
        portfolio = Portfolio.objects.get(slug=slug)
        if portfolio.user != user:
            return redirect('home', slug=slug)
        post = Post.objects.get(url=name)
        # form = PostForm(request.POST)
        # form.errors.clear()
        # if form.is_valid():
        #     post = form.save(commit=False)
        #     portfolio = Portfolio.objects.get(slug=slug)
        #     post.portfolio = portfolio
        #     post.description = form.cleaned_data['description']
        #     post.home_image = request.FILES['home_image']
        #     post.save()
        #     for f in self.request.FILES.getlist('files'):
        #         data = f.read()
        #         photo = Photo(post=post)
        #         photo.file.save(f.name, ContentFile(data))
        #         photo.save()
        #     return redirect(post.get_absolute_url())


class PostDeleteView(View):

    def get(self, request, slug, name):
        user = request.user
        portfolio = Portfolio.objects.get(slug=slug)
        if portfolio.user != user:
            return redirect('portfolio:home', slug=slug)
        post = Post.objects.get(url=name)
        context = {'post': post, 'portfolio': portfolio}
        return render(request, 'photo_blog_constructor/delete_post.html', context)

    def post(self, request, slug, name):
        user = request.user
        portfolio = Portfolio.objects.get(slug=slug)
        if portfolio.user != user:
            return redirect('home', slug=slug)
        post = Post.objects.get(url=name)
        post.delete()
        return redirect('portfolio:post_statistics', slug=portfolio.slug)


@login_required
def reader_view(request, slug):
    portfolio = Portfolio.objects.get(slug=slug)
    if portfolio.user != request.user:
        return redirect('portfolio:home', slug=slug)
    readers = Reader.objects.filter(portfolio=portfolio)
    if request.method == 'POST':
        readers_id = request.POST.getlist('black')
        for reader in readers_id:
            black = readers.get(pk=reader)
            black.is_blocked = True
            black.save()
            return redirect('portfolio:readers', slug=portfolio.slug)
    context = {'portfolio': portfolio, 'readers': readers}
    return render(request, 'photo_blog_constructor/readers.html', context)


@is_reader
def about_view(request, slug):
    portfolio = Portfolio.objects.get(slug=slug)
    form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        del form.errors['portfolio']
        if form.is_valid():
            message = form.save(commit=False)
            message.portfolio = portfolio
            form.save()
            return redirect('portfolio:home', slug=portfolio.slug)
    context = {'portfolio': portfolio, 'form': form}
    return render(request, 'photo_blog_constructor/about.html', context)


@login_required
def message_view(request, slug):
    user = request.user
    portfolio = Portfolio.objects.get(slug=slug)
    if portfolio.user != user:
        return redirect('portfolio:home', slug=slug)
    messages = Contact.objects.filter(portfolio=portfolio)
    context = {'portfolio': portfolio, 'messages': messages}
    return render(request, 'photo_blog_constructor/message.html', context)


@login_required
def message_detail(request, slug, pk):
    user = request.user
    portfolio = Portfolio.objects.get(slug=slug)
    if portfolio.user != user:
        return redirect('portfolio:home', slug=slug)
    message = Contact.objects.get(pk=pk)
    if message.is_read:
        context = {'portfolio': portfolio, 'message': message}
        return render(request, 'photo_blog_constructor/message_detail.html', context)
    else:
        message.is_read = True
        message.save()
        context = {'portfolio': portfolio, 'message': message}
        return render(request, 'photo_blog_constructor/message_detail.html', context)


@login_required
def delete_message(request, slug, pk):
    user = request.user
    portfolio = Portfolio.objects.get(slug=slug)
    if portfolio.user != user:
        return redirect('portfolio:home', slug=slug)
    message = Contact.objects.get(pk=pk)
    if request.method == 'POST':
        message.delete()
        return redirect('portfolio:messages', slug=slug)
    context = {'portfolio': portfolio, 'message': message}
    return render(request, 'photo_blog_constructor/delete_message.html', context)


@login_required
def info_portfolio(request, slug):
    user = request.user
    portfolio = Portfolio.objects.get(slug=slug)
    if portfolio.user != user:
        return redirect('portfolio:home', slug=slug)
    form = PortfolioForm(instance=portfolio)
    if request.method == 'POST':
        form = PortfolioForm(request.POST or None, instance=portfolio)
        if form.is_valid():
            form.save()
            return redirect('portfolio:home', slug=portfolio.slug)
    context = {'portfolio': portfolio, 'form': form}
    return render(request, 'photo_blog_constructor/edit_profile.html', context)


def category_view(request, slug):
    user = request.user
    portfolio = Portfolio.objects.get(slug=slug)
    if portfolio.user != user:
        return redirect('portfolio:home', slug=slug)
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.portfolio = portfolio
            category.save()
            return redirect('portfolio:add_category', slug=portfolio.slug)
    context = {'portfolio': portfolio, 'form': form}
    return render(request, 'photo_blog_constructor/add_category.html', context)
