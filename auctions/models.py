from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    pass

    def __str__(self):
        return self.username


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=1000)
    starting_bid = models.FloatField()
    image = models.URLField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    terminated = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=CASCADE)
    category = models.ForeignKey(
        Category, on_delete=SET_NULL, blank=False, null=True)
    winner = models.ForeignKey(
        User, blank=True, null=True, related_name='winner', on_delete=CASCADE)
    watching = models.ManyToManyField(
        User, related_name='watch_list', blank=True, null=True)

    def __str__(self):
        return self.title


class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    amount = models.FloatField()
    listing = models.ForeignKey(Listing, on_delete=CASCADE)
    user = models.ForeignKey(User, on_delete=CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}: {self.amount} on {self.listing}'


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    body = models.CharField(max_length=300)
    listing = models.ForeignKey(Listing, on_delete=CASCADE)
    user = models.ForeignKey(User, on_delete=CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} on {self.listing}: {self.body} | created: {self.created} / modified: {self.modified}'
