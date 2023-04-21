from django.db import models
from django.contrib.auth.models import AbstractUser


class Location(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    lat = models.FloatField(verbose_name="Широта")
    lng = models.FloatField(verbose_name="Долгота")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"


class User(AbstractUser):
    MEMBER = "member"
    MODERATOR = "moderator"
    ADMIN = "admin"
    STATUS = [
        (MEMBER, "Гость"),
        (MODERATOR, "Модератор"),
        (ADMIN, "Администратор")
    ]
    role = models.CharField(max_length=9, verbose_name="Роль", default="member", choices=STATUS)
    age = models.PositiveSmallIntegerField(null=True, verbose_name="Возраст")
    locations = models.ManyToManyField(Location, verbose_name="Локация")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"



