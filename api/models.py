from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    
    USERNAME_FIELD = 'username'
    
    username = models.CharField("Короткая ссылка", max_length=15, unique=True)
    email = models.EmailField("Почта", unique=True)
    password = models.CharField("Пароль", max_length=128)
    description = models.TextField("Описание профиля")
    first_name = models.CharField("Имя", max_length=15)
    last_name = models.CharField("Фамилия", max_length=20)

    def __str__(self):
        return f"{self.username}: {self.first_name} {self.last_name}"


class BusinessCard(models.Model):

    owner_id = models.IntegerField("Айди создателя", null=True)
    role = models.CharField("Роль человека", max_length=19)
    phone = models.CharField("Номер телефона", max_length=19)
    
    # Urls
    own_site = models.CharField("Сайт человека", max_length=120)
    linkedin_url = models.CharField("Ссылка на Линкдин", max_length=120)
    telegram_url = models.CharField("Ссылка на Телеграм", max_length=120)

    @property
    def first_name(self):
        o = User.objects.filter(id=self.owner_id).first()
        if not o:
            return "Can't find user"
        return o.first_name

    def __str__(self):
        return f"{self.first_name} - {self.role}: {self.phone} / ({self.own_site}, {self.linkedin_url}, {self.telegram_url})"    