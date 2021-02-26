from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.db.models import F
from django.shortcuts import render, redirect
from django.views.generic import View

from .forms import PostForm, CommentForm, ContactForm
from .models import Portfolio, Post, Comment, Reader, Photo, Contact


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
        post.views = F('views') + 1
        post.save()
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


# class ReaderView(View):
#
#     def get(self, request, slug):
#         form = ReaderRegistrationForm()
#         portfolio = Portfolio.objects.get(slug=slug)
#         context = {'portfolio': portfolio, 'form': form}
#         return render(request, 'photo_blog_constructor/register.html', context)
#
#     def post(self, request, slug):
#         portfolio = Portfolio.objects.get(slug=slug)
#         form = ReaderRegistrationForm(request.POST)
#         if form.is_valid():
#             new_user = form.save(commit=False)
#             new_user.set_password(form.cleaned_data['password'])
#             new_user.save()
#             reader = Reader.objects.create(user=new_user, portfolio=portfolio)
#             reader.save()
#             return redirect(portfolio.get_absolute_url())
#         else:
#             form = ReaderRegistrationForm()
#             context = {'portfolio': portfolio, 'form': form}
#             return render(request, 'photo_blog_constructor/register.html', context)


class ProfileView(View):

    def get(self, request, slug):
        portfolio = Portfolio.objects.get(slug=slug)
        return render(request, 'photo_blog_constructor/profile.html', {'portfolio': portfolio})


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
            return redirect('home', slug=slug)
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
        return redirect('post_statistics', slug=portfolio.slug)


# class ReaderView(View):
#
#     def get(self, request, slug):
#         user = request.user
#         portfolio = Portfolio.objects.get(slug=slug)
#         if portfolio.user != user:
#             return redirect('home', slug=slug)
#         readers = Reader.objects.filter(portfolio=portfolio)
#         context = {'portfolio': portfolio, 'readers': readers}
#         return render(request, 'photo_blog_constructor/readers.html', context)
#
#     def post(self, request, slug):
#         user = request.user
#         portfolio = Portfolio.objects.get(slug=slug)
#         if portfolio.user != user:
#             return redirect('home', slug=slug)
#         readers_id = request.POST.getlist('black')
#         for reader in readers_id:
#             if
#         # for reader in readers_id:

@login_required
def reader_view(request, slug):
    portfolio = Portfolio.objects.get(slug=slug)
    if portfolio.user != request.user:
        return redirect('home', slug=slug)
    readers = Reader.objects.filter(portfolio=portfolio)
    if request.method == 'POST':
        readers_id = request.POST.getlist('black')
        for reader in readers_id:
            black = readers.get(pk=reader)
            black.is_blocked = True
            black.save()
            return redirect('readers', slug=portfolio.slug)
    context = {'portfolio': portfolio, 'readers': readers}
    return render(request, 'photo_blog_constructor/readers.html', context)


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
        return redirect('home', slug=slug)
    messages = Contact.objects.filter(portfolio=portfolio)
    context = {'portfolio': portfolio, 'messages': messages}
    return render(request, 'photo_blog_constructor/message.html', context)


@login_required
def message_detail(request, slug, pk):
    user = request.user
    portfolio = Portfolio.objects.get(slug=slug)
    if portfolio.user != user:
        return redirect('home', slug=slug)
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
        return redirect('home', slug=slug)
    message = Contact.objects.get(pk=pk)
    if request.method == 'POST':
        message.delete()
        return redirect('portfolio:messages', slug=slug)
    context = {'portfolio': portfolio, 'message': message}
    return render(request, 'photo_blog_constructor/delete_message.html', context)
