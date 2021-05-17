from django.contrib.auth.models import User
from django.db import models


class City(models.Model):
    name = models.CharField(max_length=64)


class Category(models.Model):
    name = models.CharField(max_length=64)


class Restaurant(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    street = models.CharField(max_length=128)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)


class Table(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    size = models.SmallIntegerField(null=False)
    window_view = models.BooleanField(default=False)
    outside = models.BooleanField(default=False)


class Reservation(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    time_from = models.DateTimeField(null=False)
    time_to = models.DateTimeField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Rating(models.Model):
    VOTES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4)
    )
    vote = models.SmallIntegerField(choices=VOTES)
    comment = models.TextField(null=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
