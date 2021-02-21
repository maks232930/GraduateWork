from django.db import models
from django.urls import reverse
from django.utils import timezone

from users.models import User


class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Имя', max_length=30, unique=True)
    slug = models.SlugField(max_length=30, unique=True)
    description = models.TextField(verbose_name='Описание блога')
    logo = models.ImageField(verbose_name='Логотип', upload_to='logo/')
    logo_ico = models.ImageField(verbose_name='Логотип ico', upload_to='logo/ico/')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Портфолио'
        verbose_name_plural = 'Портфолио'


class Reader(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)

    def __str__(self):
        return f'Читатель {self.user.get_full_name()} блога {self.portfolio.name}'

    class Meta:
        verbose_name = 'Читатель'
        verbose_name_plural = 'Читатели'


class Category(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Имя категории', max_length=30)
    slug = models.SlugField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Post(models.Model):
    title = models.CharField(verbose_name='Название', max_length=50)
    url = models.SlugField(max_length=50, unique=True, blank=True)
    description = models.TextField(verbose_name='Описание', max_length=10000000)
    home_image = models.ImageField(verbose_name='Фото на главную', upload_to='photo/home/%Y/%m/%d/', blank=True)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    date = models.DateField(verbose_name='Дата', default=timezone.now)
    views = models.PositiveIntegerField('Просмотры', default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.portfolio.slug, 'name': self.url})

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Photo(models.Model):
    post = models.ForeignKey(Post, verbose_name='Пост', on_delete=models.CASCADE)
    file = models.FileField('Вложения', upload_to='attachments', blank=True)

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'


class Comment(models.Model):
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True)
    content = models.TextField(max_length=1000)
    date = models.DateTimeField(verbose_name='Дата', auto_now_add=True)

    def __str__(self):
        return f'{self.reader.user.get_full_name()} {self.post}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class BlackList(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)

    def __str__(self):
        return f'Читатель {self.reader.user.get_full_name()} заблокирован на {self.portfolio.name}'

    class Meta:
        verbose_name = 'Черный список'
        verbose_name_plural = 'Черные списки'


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)

    def __str__(self):
        return f'лайк {self.reader.user.get_full_name()} на пост {self.post.title}'

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'


class SocialLink(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)

    SOCIAL_LINK = [
        ('vk', 'Vk'),
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('dribbble', 'Dribbble'),
        ('amazon', 'Amazon'),
        ('github', 'Github'),
        ('instagram', 'Instagram'),
        ('skype', 'Skype'),
        ('youtube-1', 'Youtube'),
        ('linkedin', 'Linkedin')
    ]
    name = models.CharField(verbose_name='Имя соцсети', choices=SOCIAL_LINK, max_length=15)
    link = models.URLField('Ссылка на соцсеть')

    def __str__(self):
        return f'{self.name} {self.link}'

    class Meta:
        verbose_name = "Соцсеть"
        verbose_name_plural = "Соцсети"
