"""ClickAndTable URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from click_and_table.views import Indexview, RestaurantListView, RestaurantDetailsView, ContactView, \
    HelpView, AdminView, AddRestaurantView, AddCategoryView, AddCityView, AdminRestaurantsView, AdminCategoriesView, \
    AdminCitiesView, EditRestaurantView, EditCategoryView, EditCityView, DeleteCityView, DeleteRestaurantView, \
    DeleteCategoryView, AdminTablesView, AddTableView, EditTableView, DeleteTableView
    # ReservationView

urlpatterns = [
    path('admin/', admin.site.urls),
    # -------------ACCOUNTS-------------#
    path('accounts/', include('accounts.urls')),
    # -------------MAIN APP-------------#
    path('', Indexview.as_view(), name="index"),
    path('restaurant_list/', RestaurantListView.as_view(), name="restaurant_list"),
    path('restaurant_details/<int:id>/', RestaurantDetailsView.as_view(), name="restaurant_details"),
    path('contact_us/', ContactView.as_view(), name="contact_us"),
    path('help/', HelpView.as_view(), name="help"),
    # path('reservation/<int:id>', ReservationView.as_view(), name="reservation"),
    # -------------ADMIN TOOLS-------------#
    path('admin_tools/', AdminView.as_view(), name="admin_tools"),
    path('admin_restaurants/', AdminRestaurantsView.as_view(), name="admin_restaurants"),
    path('admin_categories/', AdminCategoriesView.as_view(), name="admin_categories"),
    path('admin_cities/', AdminCitiesView.as_view(), name="admin_cities"),
    path('restaurant_add/', AddRestaurantView.as_view(), name="restaurant_add"),
    path('category_add/', AddCategoryView.as_view(), name="category_add"),
    path('city_add/', AddCityView.as_view(), name="city_add"),
    path('restaurant_edit/<int:pk>/', EditRestaurantView.as_view(), name="restaurant_edit"),
    path('category_edit/<int:pk>/', EditCategoryView.as_view(), name="category_edit"),
    path('city_edit/<int:pk>/', EditCityView.as_view(), name="city_edit"),
    path('restaurant_delete/<int:id>/', DeleteRestaurantView.as_view(), name="restaurant_delete"),
    path('category_delete/<int:id>/', DeleteCategoryView.as_view(), name="category_delete"),
    path('city_delete/<int:id>/', DeleteCityView.as_view(), name="city_delete"),
    path('restaurant/<int:id>/admin_tables/', AdminTablesView.as_view(), name="admin_tables"),
    path('restaurant/<int:id>/table_add/', AddTableView.as_view(), name="table_add"),
    path('restaurant/<int:pk>/table_edit/', EditTableView.as_view(), name="table_edit"),
    path('restaurant/<int:id>/table_delete/', DeleteTableView.as_view(), name="table_delete"),
]
