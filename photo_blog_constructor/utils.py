from django.shortcuts import redirect

from .models import Reader, Portfolio


def is_reader(func):
    def wrapper(request, slug, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            portfolio = Portfolio.objects.get(slug=slug)
            reader = Reader.objects.filter(portfolio=portfolio, user=user).first()
            if reader is not None:
                if reader.is_blocked:
                    return redirect('users:home')
                return func(request, slug, *args, **kwargs)
            else:
                reader = Reader.objects.create(portfolio=portfolio, user=user)
                reader.save()
                return func(request, slug, *args, **kwargs)
        return func(request, slug, *args, **kwargs)

    return wrapper


class ReaderMixin:

    def is_reader(self, request, slug):
        if request.user.is_authenticated:
            user = request.user
            portfolio = Portfolio.objects.get(slug=slug)
            reader = Reader.objects.filter(portfolio=portfolio, user=user).first()
            if reader is not None:
                if reader.is_blocked:
                    return False
                return True
            elif portfolio.user == user:
                return True
            else:
                reader = Reader.objects.create(portfolio=portfolio, user=user)
                reader.save()
                return True
        return True
