from datetime import datetime

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView
from .filters import RestaurantFilter
from click_and_table.forms import RestaurantForm, CategoryForm, CityForm, TableForm, ReservationForm
from click_and_table.models import Category, City, Restaurant, Table, Rating  # Reservation


class Indexview(View):
    def get(self, request):
        return render(request, '__base__.html')


class RestaurantListView(View):
    def get(self, request):
        restaurants = Restaurant.objects.all()
        my_filter = RestaurantFilter(request.GET, queryset=restaurants)
        restaurants = my_filter.qs
        my_search = RestaurantFilter(request.GET, queryset=restaurants)
        restaurants = my_search.qs
        return render(request, 'restaurant_list.html', {'restaurants': restaurants, 'my_filter': my_filter})


class RestaurantDetailsView(View):
    def get(self, request, id):
        restaurant = Restaurant.objects.get(id=id)
        rating_1 = Rating.objects.filter(restaurant_id=id)[0]
        ratings = Rating.objects.filter(restaurant_id=id)[1:]
        avg_rating = restaurant.average_rating()
        return render(request, 'restaurant_details.html',
                      {'restaurant': restaurant, 'avg_rating': avg_rating, 'rating_1': rating_1, 'ratings': ratings})

    def post(self, request, id):
        restaurant = Restaurant.objects.get(id=id)
        vote = request.POST.get('star')
        comment = request.POST.get('comment')
        user = request.user
        Rating.objects.create(vote=vote, comment=comment, user=user, restaurant=restaurant)
        return render(request, 'restaurant_details.html', {'restaurant': restaurant})


class ContactView(View):
    def get(self, request):
        return render(request, 'contact_us.html')


class HelpView(View):
    def get(self, request):
        return render(request, 'help.html')


# class ReservationView(View):
#     def get(self, request, id):
#         restaurant = Restaurant.objects.get(pk=id)
#         form = ReservationForm
#         return render(request, 'reservation_form.html', {'form': form, 'restaurant': restaurant})

# def post(self, request, id):
#     table =
#     time_from_str = datetime.strptime(request.POST.get('time_from'), '%d-%m-%Y %H:%M')
#     time_to_str = datetime.strptime(request.POST.get('time_to'), '%d-%m-%Y %H:%M')
#     time_now = datetime.now()
#     if Reservation.objects.filter(restaurant_id=id, table=table, time_from=time_from_str, time_to=time_to_str).exists():
#         return HttpResponse('Table not available')
#     elif date_str < time_now:
#         return HttpResponse('Cannot make a reservation in the past')
#     else:
#         reservation = Reservation(table=table, restaurant_id=id)
#         reservation.save()
#         return redirect('/room_list/')


# ------------------------------------- ADMIN TOOLS -------------------------------------------------------------

class AdminView(PermissionRequiredMixin, View):
    permission_required = ['click_and_table.change_restaurant', 'click_and_table.add_restaurant',
                           'click_and_table.delete_restaurant', 'click_and_table.change_category',
                           'click_and_table.add_category', 'click_and_table.delete_category',
                           'click_and_table.change_city', 'click_and_table.add_city', 'click_and_table.delete_city',
                           'click_and_table.change_table', 'click_and_table.add_table', 'click_and_table.delete_table']

    def get(self, request):
        return render(request, 'admin_tools.html')


class AdminRestaurantsView(View):
    def get(self, request):
        restaurants = Restaurant.objects.all()
        return render(request, 'admin_restaurants.html', {'restaurants': restaurants})


class AdminCategoriesView(View):
    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'admin_categories.html', {'categories': categories})


class AdminCitiesView(View):
    def get(self, request):
        cities = City.objects.all()
        return render(request, 'admin_cities.html', {'cities': cities})


class AdminTablesView(View):
    def get(self, request, id):
        restaurant = Restaurant.objects.get(pk=id)
        tables = Table.objects.filter(restaurant_id=restaurant.id)
        return render(request, 'admin_tables.html', {'tables': tables, 'restaurant': restaurant})


class AddRestaurantView(PermissionRequiredMixin, View):
    permission_required = ['click_and_table.add_restaurant']

    def get(self, request):
        form = RestaurantForm
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        restaurants = Restaurant.objects.all()
        form = RestaurantForm(request.POST)
        if form.is_valid():
            form.save()
        return render(request, 'admin_restaurants.html', {'restaurants': restaurants})


class EditRestaurantView(PermissionRequiredMixin, UpdateView):
    permission_required = ['click_and_table.change_restaurant']

    model = Restaurant
    fields = '__all__'
    success_url = reverse_lazy('admin_restaurants')
    template_name = 'form.html'


class DeleteRestaurantView(PermissionRequiredMixin, View):
    permission_required = ['click_and_table.delete_restaurant']

    def get(self, request, id):
        restaurant = Restaurant.objects.get(id=id)
        return render(request, 'admin_delete.html', {'object': restaurant})

    def post(self, request, id):
        restaurants = Restaurant.objects.all()
        if request.POST.get('answer') == "Yes":
            restaurant = Restaurant.objects.get(id=id)
            restaurant.delete()
            return render(request, 'admin_restaurants.html', {'restaurants': restaurants})
        return render(request, 'admin_restaurants.html', {'restaurants': restaurants})


class AddCategoryView(PermissionRequiredMixin, View):
    permission_required = ['click_and_table.add_category']

    def get(self, request):
        form = CategoryForm
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        categories = Category.objects.all()
        form = CategoryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            Category.objects.create(name=name)
        return render(request, 'admin_categories.html', {'categories': categories})


class EditCategoryView(PermissionRequiredMixin, UpdateView):
    permission_required = ['click_and_table.change_category']

    model = Category
    fields = '__all__'
    success_url = reverse_lazy('admin_categories')
    template_name = 'form.html'


class DeleteCategoryView(View):
    permission_required = ['click_and_table.delete_category']

    def get(self, request, id):
        category = Category.objects.get(id=id)
        return render(request, 'admin_delete.html', {'object': category})

    def post(self, request, id):
        categories = Category.objects.all()
        if request.POST.get('answer') == "Yes":
            category = Category.objects.get(id=id)
            category.delete()
            return render(request, 'admin_categories.html', {'categories': categories})
        return render(request, 'admin_categories.html', {'categories': categories})


class AddCityView(PermissionRequiredMixin, View):
    permission_required = ['click_and_table.add_city']

    def get(self, request):
        form = CityForm
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        cities = City.objects.all()
        form = CityForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            City.objects.create(name=name)
        return render(request, 'admin_cities.html', {'cities': cities})


class EditCityView(PermissionRequiredMixin, UpdateView):
    permission_required = ['click_and_table.change_city']

    model = City
    fields = '__all__'
    success_url = reverse_lazy('admin_cities')
    template_name = 'form.html'


class DeleteCityView(View):
    permission_required = ['click_and_table.delete_city']

    def get(self, request, id):
        city = City.objects.get(id=id)
        return render(request, 'admin_delete.html', {'object': city})

    def post(self, request, id):
        cities = City.objects.all()
        if request.POST.get('answer') == "Yes":
            city = City.objects.get(id=id)
            city.delete()
            return render(request, 'message_template.html', {'msg': 'City deleted'})
        return render(request, 'admin_cities.html', {'cities': cities})


class AddTableView(PermissionRequiredMixin, View):
    permission_required = ['click_and_table.add_table']

    def get(self, request, id):
        restaurant = Restaurant.objects.get(pk=id)
        form = TableForm(initial={'restaurant': restaurant.id})
        return render(request, 'form.html', {'form': form})

    def post(self, request, id):
        restaurant = Restaurant.objects.get(pk=id)
        tables = Table.objects.filter(restaurant_id=id)
        form = TableForm(request.POST)
        if form.is_valid():
            form.save()
        return render(request, 'admin_tables.html', {'tables': tables, 'restaurant': restaurant})


class EditTableView(PermissionRequiredMixin, UpdateView):
    permission_required = ['click_and_table.change_table']

    model = Table
    fields = '__all__'
    template_name = 'form.html'


class DeleteTableView(PermissionRequiredMixin, View):
    permission_required = ['click_and_table.delete_table']

    def get(self, request, id):
        table = Table.objects.get(id=id)
        return render(request, 'admin_delete.html', {'object': table})

    def post(self, request, id):
        restaurant = Restaurant.objects.get(pk=id)
        tables = Table.objects.filter(restaurant_id=id)
        if request.POST.get('answer') == "Yes":
            table = Table.objects.get(id=id)
            table.delete()
            return render(request, 'admin_tables.html', {'tables': tables, 'restaurant': restaurant})
        tables = Restaurant.objects.all()
        return render(request, 'admin_tables.html', {'tables': tables})
