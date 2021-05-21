import random
import string

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg
from django.urls import reverse_lazy


class City(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    def average_rating(self):
        avg = Rating.objects.filter(restaurant=self).aggregate(Avg('vote'))
        return avg['vote__avg']

    name = models.CharField(max_length=128)
    description = models.TextField()
    street = models.CharField(max_length=128)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class Table(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    size = models.SmallIntegerField(null=False)
    window_view = models.BooleanField(default=False)
    outside = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse_lazy('admin_tables', kwargs={'id': self.restaurant.id})


def generate_reservation_code(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class Reservation(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    time_from = models.TimeField(auto_now=False, auto_now_add=False, null=True)
    time_to = models.TimeField(auto_now=False, auto_now_add=False, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reservation_code = models.CharField(max_length=64, default=generate_reservation_code)


class Rating(models.Model):
    vote = models.SmallIntegerField(default=0)
    comment = models.TextField(null=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def vote_to_list(self):
        vote_lst = []
        for x in range(self.vote):
            vote_lst.append(1)
        return vote_lst
