import random
from random import choice

import pytest
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from faker import Factory

from click_and_table.models import City, Category, Restaurant, Rating, Table

faker = Factory.create()


@pytest.fixture
def user():
    u = User()
    u.username = 'alli'
    u.set_password("password")
    u.save()
    return u


@pytest.fixture
def user_perm_restaurant():
    user = User.objects.create(username='alli', password='1234')
    change_user_permissions = Permission.objects.filter(
        codename__in=['add_restaurant', 'change_restaurant', 'delete_restaurant'])
    user.user_permissions.add(*change_user_permissions)
    return user


@pytest.fixture
def user_perm_city():
    user = User.objects.create(username='alli', password='1234')
    change_user_permissions = Permission.objects.filter(
        codename__in=['add_city', 'change_city', 'delete_city'])
    user.user_permissions.add(*change_user_permissions)
    return user


@pytest.fixture
def user_perm_category():
    user = User.objects.create(username='alli', password='1234')
    change_user_permissions = Permission.objects.filter(
        codename__in=['add_category', 'change_category', 'delete_category'])
    user.user_permissions.add(*change_user_permissions)
    return user


@pytest.fixture
def user_perm_table():
    user = User.objects.create(username='alli', password='1234')
    change_user_permissions = Permission.objects.filter(
        codename__in=['add_table', 'change_table', 'delete_table'])
    user.user_permissions.add(*change_user_permissions)
    return user


@pytest.fixture
def user_perm_admin():
    user = User.objects.create(username='alli', password='1234')
    change_user_permissions = Permission.objects.filter(
        codename__in=['add_restaurant', 'change_restaurant', 'delete_restaurant', 'add_category', 'change_category',
                      'delete_category', 'add_city', 'change_city', 'delete_city'])
    user.user_permissions.add(*change_user_permissions)
    return user


@pytest.fixture
def category():
    cat = Category()
    cat.name = "Category"
    cat.save()
    return cat


@pytest.fixture
def categories():
    cat_lst = []
    for x in range(5):
        cat = Category()
        cat.name = f"Category{x}"
        cat.save()
        cat_lst.append(cat)
    return cat_lst


@pytest.fixture
def city():
    city = City()
    city.name = faker.city()
    city.save()
    return city


@pytest.fixture
def cities():
    city_lst = []
    for x in range(5):
        city = City()
        city.name = faker.city()
        city.save()
        city_lst.append(city)
    return city_lst


@pytest.fixture
def ratings():
    ratings = []
    n = random.randint(1, 9)
    for x in range(n):
        r = Rating()
        r.vote = random.randint(1, 5)
        r.comment = "some comment"
        ratings.append(r)
    return ratings


@pytest.fixture
def restaurant(cities, categories):
    r = Restaurant()
    r.id = random.randint(1, 99)
    r.name = faker.name()
    r.description = 'some description'
    r.street = 'some street'
    r.city = choice(cities)
    r.category.set([categories[0].pk, categories[1].pk])
    r.image = 'no_picture.jpg'
    r.save()
    return r


@pytest.fixture
def restaurants(cities, categories, ratings):
    r_list = []
    for _ in range(5):
        r = Restaurant()
        r.id = f"{_}"
        r.name = faker.name()
        r.description = 'some description'
        r.street = 'some street'
        r.city = choice(cities)
        r.category.set([categories[0].pk, categories[1].pk])
        r.image = 'no_picture.jpg'
        r.save()
        r_list.append(r)
    return r_list


@pytest.fixture
def table(restaurants):
    t = Table()
    t.size = random.randint(2, 8)
    t.restaurant = choice(restaurants)
    t.window = False
    t.garden = True
    t.save()
    return t


@pytest.fixture
def tables(restaurants):
    table_lst = []
    for x in range(4):
        t = Table()
        t.size = random.randint(2, 8)
        t.restaurant = choice(restaurants)
        t.window = False
        t.garden = True
        t.save()
        table_lst.append(t)
    return table_lst

