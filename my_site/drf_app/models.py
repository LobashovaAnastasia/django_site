from django.db import models
from django.contrib.auth.models import User, BaseUserManager
from django.core.mail import send_mail
from my_site.settings import DEFAULT_FROM_EMAIL


class Publisher(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()


class Book(models.Model):
    name = models.CharField(max_length=300)
    price = models.IntegerField(default=0)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    authors = models.ManyToManyField(Author)

    class Meta:
        default_related_name = 'books'

    def __str__(self):
        return f'{self.name}, {self.price} $, [publisher: {self.publisher}]'


class Store(models.Model):
    name = models.CharField(max_length=300)
    books = models.ManyToManyField(Book)

    class Meta:
        default_related_name = 'stores'

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, *args, **kwargs):
        response = super().create_user(username, email, password, *args, **kwargs)
        send_mail(subject="Account active",
                  message="Your account is active",
                  from_email=DEFAULT_FROM_EMAIL,
                  recipient_list=[email]
                  )


class CustomUser(User):
    objects = UserManager()

