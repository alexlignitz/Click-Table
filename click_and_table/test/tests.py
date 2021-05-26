import datetime
from random import choice

import pytest
from django.test import Client
from django.urls import reverse
from faker import Factory
from click_and_table.test.conftest import cities, categories, city, table

faker = Factory.create()


@pytest.mark.django_db
def test_client():
    Client()


# ---- INDEX ----

@pytest.mark.django_db
def test_index_view_get():
    c = Client()
    url = reverse('index')
    response = c.get(url)
    assert response.status_code == 200


#  ---- RESTAURANT LIST ----

@pytest.mark.django_db
def test_restaurant_list_view_get(restaurants):
    c = Client()
    url = reverse('restaurant_list')
    response = c.get(url)
    restaurants = response.context['restaurants']
    assert response.status_code == 200
    assert restaurants.count() == len(restaurants)


# ---- RESTAURANT DETAILS ----

@pytest.mark.django_db
def test_restaurant_details(restaurant):
    c = Client()
    url = reverse('restaurant_details', args=[restaurant.id])
    response = c.get(url)
    assert response.status_code == 200


# ---- RESERVATION ----

@pytest.mark.django_db
def test_view_reservations_no_login(user, reservations):
    c = Client()
    url = reverse('my_account')
    response = c.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_view_reservations_login(user, reservations):
    c = Client()
    url = reverse('my_account')
    c.force_login(user)
    response = c.get(url)
    reservations = response.context['reservations']
    assert response.status_code == 200
    assert reservations.count() == len(reservations)


@pytest.mark.django_db
def test_add_reservation_no_login(user, restaurant):
    c = Client()
    url = reverse('reservation', args=[restaurant.id])
    response = c.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_add_reservation_login_get(user, restaurant):
    c = Client()
    url = reverse('reservation', args=[restaurant.id])
    c.force_login(user)
    response = c.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_reservation_login_post(user, table):
    c = Client()
    url = reverse('reservation', args=[table.restaurant.id])
    c.force_login(user)
    ctx = {
        'restaurant': table.restaurant.id,
        'table': table.restaurant.id,
        'date': datetime.date.today() + datetime.timedelta(days=1),
        'time_from': '17:00',
        'time_to': '19:00',
        'user': user,
    }
    response = c.post(url, ctx)
    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_reservation_no_login(user, reservation):
    c = Client()
    url = reverse('reservation_edit', args=[reservation.id])
    response = c.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_edit_reservation_login_get(user, reservation):
    c = Client()
    url = reverse('reservation_edit', args=[reservation.id])
    c.force_login(user)
    response = c.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_reservation_login_post(user, reservation, restaurants, tables):
    c = Client()
    url = reverse('reservation_edit', args=[reservation.id])
    c.force_login(user)
    ctx = {
        'table': reservation.table,
        'date': datetime.date.today() + datetime.timedelta(days=1),
        'time_from': '18:00',
        'time_to': '20:00',
    }
    response = c.get(url, ctx)
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_reservation_no_login(user, reservation):
    c = Client()
    url = reverse('reservation_delete', args=[reservation.id])
    response = c.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_delete_reservation_login_get(user, reservation):
    c = Client()
    url = reverse('reservation_delete', args=[reservation.id])
    c.force_login(user)
    response = c.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_reservation_login_post(user, reservation):
    c = Client()
    c.force_login(user)
    url = reverse('reservation_delete', args=[reservation.id])
    response = c.post(url, {'answer': 'Yes'})
    assert response.status_code == 302


#  ---- CONTACT PAGE ----

@pytest.mark.django_db
def test_contact_view():
    c = Client()
    url = reverse('contact_us')
    response = c.get(url)
    assert response.status_code == 200


#  ---- HELP PAGE ----

@pytest.mark.django_db
def test_contact_view():
    c = Client()
    url = reverse('help')
    response = c.get(url)
    assert response.status_code == 200


# ---- ADMIN TOOLS ----

@pytest.mark.django_db
def test_admin_tools_view_no_perm(user):
    c = Client()
    c.force_login(user)
    url = reverse('admin_tools')
    response = c.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_admin_tools_with_perm(user_perm_admin):
    c = Client()
    c.force_login(user_perm_admin)
    url = reverse('admin_tools')
    response = c.get(url)
    assert response.status_code == 200


# ---- ADMIN RESTAURANT ----

@pytest.mark.django_db
def test_restaurant_view_admin(user, restaurants):
    c = Client()
    c.force_login(user)
    url = reverse('admin_restaurants')
    response = c.get(url)
    restaurants = response.context['restaurants']
    assert response.status_code == 200
    assert restaurants.count() == len(restaurants)


@pytest.mark.django_db
def test_add_restaurant_no_perm(user):
    c = Client()
    c.force_login(user)
    url = reverse('restaurant_add')
    response = c.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_add_restaurant_with_perm(user_perm_restaurant):
    c = Client()
    c.force_login(user_perm_restaurant)
    url = reverse('restaurant_add')
    response = c.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_restaurant_with_perm_post(user_perm_restaurant):
    c = Client()
    c.force_login(user_perm_restaurant)
    url = reverse('restaurant_add')
    ctx = {
        'name': faker.name(),
        'description': 'some description',
        'street': 'some street',
        'city': city,
        'category': ['Category1', 'Category2'],
        'image': 'None'
    }
    response = c.post(url, ctx)
    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_restaurant_no_perm(user, restaurant):
    c = Client()
    c.force_login(user)
    url = reverse('restaurant_edit', args=[restaurant.id])
    response = c.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_edit_restaurant_with_perm_get(user_perm_restaurant, restaurant):
    c = Client()
    c.force_login(user_perm_restaurant)
    url = reverse('restaurant_edit', args=[restaurant.id])
    response = c.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_restaurant_with_perm_post(user_perm_restaurant, restaurant):
    c = Client()
    c.force_login(user_perm_restaurant)
    url = reverse('restaurant_edit', args=[restaurant.id])
    ctx = {
        'name': faker.name(),
        'description': 'some description',
        'street': 'some street',
        'city': restaurant.city,
        'category': restaurant.category,
        'image': 'None'
    }
    response = c.post(url, ctx)
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_restaurant_no_perm(user, restaurant):
    c = Client()
    c.force_login(user)
    url = reverse('restaurant_delete', args=[restaurant.id])
    response = c.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_restaurant_with_perm_get(user_perm_restaurant, restaurant):
    c = Client()
    c.force_login(user_perm_restaurant)
    url = reverse('restaurant_delete', args=[restaurant.id])
    response = c.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_restaurant_with_perm_post(user_perm_restaurant, restaurant):
    c = Client()
    c.force_login(user_perm_restaurant)
    url = reverse('restaurant_delete', args=[restaurant.id])
    response = c.post(url)
    assert response.status_code == 200


# ---- ADMIN CITY ----

@pytest.mark.django_db
def test_city_view_admin(user, cities):
    c = Client()
    c.force_login(user)
    url = reverse('admin_cities')
    response = c.get(url)
    cities = response.context['cities']
    assert response.status_code == 200
    assert cities.count() == len(cities)


@pytest.mark.django_db
def test_add_city_no_perm(user):
    c = Client()
    c.force_login(user)
    url = reverse('city_add')
    response = c.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_add_city_with_perm_get(user_perm_city):
    c = Client()
    c.force_login(user_perm_city)
    url = reverse('city_add')
    response = c.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_city_with_perm_post(user_perm_city):
    c = Client()
    c.force_login(user_perm_city)
    url = reverse('city_add')
    response = c.post(url, {'name': faker.city()})
    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_city_no_perm(user, city):
    c = Client()
    c.force_login(user)
    url = reverse('city_edit', args=[city.id])
    response = c.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_edit_city_with_perm_get(user_perm_city, city):
    c = Client()
    c.force_login(user_perm_city)
    url = reverse('city_edit', args=[city.id])
    response = c.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_city_with_perm_post(user_perm_city, city):
    c = Client()
    c.force_login(user_perm_city)
    url = reverse('city_edit', args=[city.id])
    response = c.post(url, {'name': faker.name()})
    assert response.status_code == 302


@pytest.mark.django_db
def test_delete_city_no_perm(user, city):
    c = Client()
    c.force_login(user)
    url = reverse('city_delete', args=[city.id])
    response = c.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_city_with_perm_get(user_perm_city, city):
    c = Client()
    c.force_login(user_perm_city)
    url = reverse('city_delete', args=[city.id])
    response = c.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_city_with_perm_post(user_perm_city, city):
    c = Client()
    c.force_login(user_perm_city)
    url = reverse('city_delete', args=[city.id])
    response = c.post(url)
    assert response.status_code == 200


# ---- ADMIN CATEGORY ----

@pytest.mark.django_db
def test_categories_view_admin(user, categories):
    c = Client()
    c.force_login(user)
    url = reverse('admin_categories')
    response = c.get(url)
    categories = response.context['categories']
    assert response.status_code == 200
    assert categories.count() == len(categories)


@pytest.mark.django_db
def test_add_category_no_perm(user):
    c = Client()
    c.force_login(user)
    url = reverse('category_add')
    response = c.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_add_category_with_perm_get(user_perm_category):
    c = Client()
    c.force_login(user_perm_category)
    url = reverse('category_add')
    response = c.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_category_with_perm_post(user_perm_category):
    c = Client()
    c.force_login(user_perm_category)
    url = reverse('category_add')
    response = c.post(url, {'name': "Category1"})
    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_category_no_perm(user, category):
    c = Client()
    c.force_login(user)
    url = reverse('category_edit', args=[category.id])
    response = c.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_edit_category_with_perm_get(user_perm_category, category):
    c = Client()
    c.force_login(user_perm_category)
    url = reverse('category_edit', args=[category.id])
    response = c.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_category_with_perm_post(user_perm_category, category):
    c = Client()
    c.force_login(user_perm_category)
    url = reverse('category_edit', args=[category.id])
    response = c.post(url, {'name': 'Category2'})
    assert response.status_code == 302


@pytest.mark.django_db
def test_delete_category_no_perm(user, category):
    c = Client()
    c.force_login(user)
    url = reverse('category_delete', args=[category.id])
    response = c.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_category_with_perm_get(user_perm_category, category):
    c = Client()
    c.force_login(user_perm_category)
    url = reverse('category_delete', args=[category.id])
    response = c.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_category_with_perm_post(user_perm_category, category):
    c = Client()
    c.force_login(user_perm_category)
    url = reverse('category_delete', args=[category.id])
    response = c.post(url, {'answer': 'Yes'})
    assert response.status_code == 200


# ---- ADMIN TABLES ----

@pytest.mark.django_db
def test_tables_view_admin(user, tables, restaurant):
    c = Client()
    c.force_login(user)
    url = reverse('admin_tables', args=[restaurant.id])
    response = c.get(url)
    tables = response.context['tables']
    assert response.status_code == 200
    assert tables.count() == len(tables)


@pytest.mark.django_db
def test_add_table_no_perm(user, restaurant):
    c = Client()
    c.force_login(user)
    url = reverse('table_add', args=[restaurant.id])
    response = c.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_add_table_with_perm_get(user_perm_table, restaurant):
    c = Client()
    c.force_login(user_perm_table)
    url = reverse('table_add', args=[restaurant.id])
    response = c.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_table_with_perm_post(user_perm_table, restaurant, restaurants):
    c = Client()
    c.force_login(user_perm_table)
    url = reverse('table_add', args=[restaurant.id])
    ctx = {
        'size': 4,
        'restaurant': restaurants[0],
        'window': True,
        'garden': False
    }
    response = c.post(url, ctx)
    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_table_no_perm(user, table):
    c = Client()
    c.force_login(user)
    url = reverse('table_edit', args=[table.id])
    response = c.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_edit_table_with_perm_get(user_perm_table, table):
    c = Client()
    c.force_login(user_perm_table)
    url = reverse('table_edit', args=[table.id])
    response = c.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_table_with_perm_post(user_perm_table, table, restaurants):
    c = Client()
    c.force_login(user_perm_table)
    url = reverse('table_edit', args=[table.id])
    ctx = {
        'size': 6,
        'restaurant': choice(restaurants),
        'window': False,
        'garden': True
    }
    response = c.post(url, ctx)
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_table_no_perm(user, table):
    c = Client()
    c.force_login(user)
    url = reverse('table_delete', args=[table.id])
    response = c.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_table_with_perm_get(user_perm_table, table):
    c = Client()
    c.force_login(user_perm_table)
    url = reverse('table_delete', args=[table.id])
    response = c.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_table_with_perm_post(user_perm_table, table):
    c = Client()
    c.force_login(user_perm_table)
    url = reverse('table_delete', args=[table.id])
    response = c.post(url, {'answer': 'Yes'})
    assert response.status_code == 302
