from django.db import models


class AsDictMixin:
    include_fields = []

    def as_dict(self):
        d = {}
        for field in self.__class__.include_fields:
            d[field] = getattr(d, field)
        return d


    @classmethod
    def get_last_n(cls, n=4):
        items = cls.objects.all()[:4]
        return [item.as_dict() for item in items]


class NewsArticle(models.Model, AsDictMixin):
    title = models.CharField(verbose_name='Заголовок')
    full_text = models.TextField(verbose_name='Полный текст')
    description = models.TextField(verbose_name='Краткое описание')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    modified = models.DateTimeField(auto_now=True, verbose_name='Последнее изменение')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class Filter(models.Model, AsDictMixin):
    code = models.CharField(verbose_name='Код')
    name = models.CharField(verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    modified = models.DateTimeField(auto_now=True, verbose_name='Последнее изменение')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Фильтр'
        verbose_name_plural = 'Фильтры'


class Functionality(models.Model, AsDictMixin):
    name = models.CharField(verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    modified = models.DateTimeField(auto_now=True, verbose_name='Последнее изменение')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Функционал'
        verbose_name_plural = 'Функционал'