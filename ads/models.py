from django.db import models
from users.models import User, Location


class Category(models.Model):
    name = models.CharField(max_length=20, verbose_name="Название")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Ad(models.Model):
    STATUS = [
        ("draft", "Черновик"),
        ("open", "Открытое"),
        ("closed", "Закрытое")
    ]
    name = models.CharField(max_length=100, verbose_name="Название")
    price = models.PositiveIntegerField(verbose_name="Цена")
    description = models.TextField(max_length=1000, null=True, verbose_name="Описание")
    is_published = models.BooleanField(default=False, verbose_name="Опубликовано")
    image = models.ImageField(upload_to='images/', default=None, verbose_name="Изображение", blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, verbose_name="Категория")
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, verbose_name="Локация", null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"


class Selection(models.Model):
    name = models.CharField(max_length=250)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE)
    items = models.ManyToManyField(Ad)

    class Meta:
        verbose_name = "Подборка"
        verbose_name_plural = "Подборки"

    def __str__(self):
        return self.name

