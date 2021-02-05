from django.db import models
from django.utils import timezone

from users.models import User


class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Имя', max_length=30)
    logo = models.ImageField(verbose_name='Логотип', upload_to='logo/')
    logo_ico = models.ImageField(verbose_name='Логотип ico', upload_to='logo/ico/')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Фото блог'
        verbose_name_plural = 'Фото блоги'


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
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(verbose_name='Описание', max_length=10000000)
    photo = models.FileField(verbose_name='Фото', upload_to='photo/%Y/%m/%d/')
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    full_name = models.CharField(verbose_name='ФИ', max_length=255)
    client = models.CharField(verbose_name='Клиент', max_length=40)
    budget = models.CharField(verbose_name='Бюджет', max_length=10)
    date = models.DateField(verbose_name='Дата', default=timezone.now)
    views = models.PositiveIntegerField('Просмотры', default=0)

    def __str__(self):
        return self.client

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def save(self, *args, **kwargs):
        self.full_name = self.portfolio.user.get_full_name()
        super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
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


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)


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
        ('youtube-1', 'Youtube')
    ]
    name = models.CharField(verbose_name='Имя соцсети', choices=SOCIAL_LINK, max_length=15)
    link = models.URLField('Ссылка на соцсеть')

    def __str__(self):
        return f'{self.name} {self.link}'

    class Meta:
        verbose_name = "Соцсеть"
        verbose_name_plural = "Соцсети"
