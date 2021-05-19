import random
import string

from django.contrib.auth.models import User
from django.db import models


class City(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


# def average_rating():
#     votes = Rating.objects.filter(id)
#     return sum(votes) / len(votes)


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


def generate_reservation_code(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class Reservation(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    time_from = models.DateTimeField(null=False)
    time_to = models.DateTimeField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reservation_code = models.CharField(max_length=64, default=generate_reservation_code)


class Rating(models.Model):
    VOTES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4)
    )
    vote = models.SmallIntegerField(choices=VOTES, default=3)
    comment = models.TextField(null=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
