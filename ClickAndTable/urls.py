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
from click_and_table.views import Indexview, VotingView, RestaurantListView, RestaurantDetailsView, ContactView, \
    HelpView, AdminView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', Indexview.as_view(), name="index"),
    path('voting/', VotingView.as_view(), name="voting"),
    path('restaurant_list/', RestaurantListView.as_view(), name="restaurant_list"),
    path('restaurant_details', RestaurantDetailsView.as_view(), name="restaurant_details"),
    path('contact_us', ContactView.as_view(), name="contact_us"),
    path('help', HelpView.as_view(), name="help"),
    path('admin_tools', AdminView.as_view(), name="admin_tools"),
]
