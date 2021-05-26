from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import UpdateView

from django import forms
from .filters import RestaurantFilter
from click_and_table.forms import RestaurantForm, CategoryForm, CityForm, TableForm, ReservationForm
from click_and_table.models import Category, City, Restaurant, Table, Rating, Reservation


class Indexview(View):
    def get(self, request):
        rated_restaurants = list(Restaurant.objects.filter(rating__isnull=False).distinct())
        restaurants = sorted(rated_restaurants, key=lambda x: x.average_rating(), reverse=True)
        top_5 = restaurants[0:5]
        return render(request, '__base__.html',
                      {'restaurants': restaurants, 'top_5': top_5})


class RestaurantListView(View):
    def get(self, request):
        restaurants = Restaurant.objects.all().order_by('name')
        my_filter = RestaurantFilter(request.GET, queryset=restaurants)
        restaurants = my_filter.qs
        my_search = RestaurantFilter(request.GET, queryset=restaurants)
        restaurants = my_search.qs
        return render(request, 'restaurant_list.html',
                      {'restaurants': restaurants, 'my_filter': my_filter})


class RestaurantDetailsView(View):
    def get(self, request, id):
        if Rating.objects.filter(restaurant_id=id).count() == 0:
            restaurant = Restaurant.objects.get(id=id)
            return render(request, 'restaurant_details.html',
                          {'restaurant': restaurant, 'msg': 'No comments yet'})
        else:
            restaurant = Restaurant.objects.get(id=id)
            ratings = Rating.objects.filter(restaurant_id=id).order_by('-vote')
            avg_rating = restaurant.average_rating()
            return render(request, 'restaurant_details.html',
                          {'restaurant': restaurant, 'avg_rating': avg_rating, 'ratings': ratings})

    def post(self, request, id):
        restaurant = Restaurant.objects.get(id=id)
        vote = request.POST.get('star')
        comment = request.POST.get('comment')
        user = request.user
        Rating.objects.create(vote=vote, comment=comment, user=user, restaurant=restaurant)

        if Rating.objects.filter(restaurant_id=id).count() == 0:
            restaurant = Restaurant.objects.get(id=id)
            return render(request, 'restaurant_details.html',
                          {'restaurant': restaurant, 'msg': 'No comments yet'})
        else:
            restaurant = Restaurant.objects.get(id=id)
            ratings = Rating.objects.filter(restaurant_id=id).order_by('-vote')
            avg_rating = restaurant.average_rating()
            return render(request, 'restaurant_details.html',
                          {'restaurant': restaurant, 'avg_rating': avg_rating, 'ratings': ratings})


class ContactView(View):
    def get(self, request):
        return render(request, 'contact_us.html')


class HelpView(View):
    def get(self, request):
        return render(request, 'help.html')


class ReservationView(LoginRequiredMixin, View):
    def get(self, request, id):
        restaurant = Restaurant.objects.get(pk=id)
        ReservationForm.base_fields['table'] = forms.ModelChoiceField(queryset=Table.objects.filter(restaurant_id=id))
        form = ReservationForm
        return render(request, 'reservation_form.html', {'form': form, 'restaurant': restaurant})

    def post(self, request, id):
        restaurant = Restaurant.objects.get(pk=id)
        ReservationForm.base_fields['table'] = forms.ModelChoiceField(queryset=Table.objects.filter(restaurant_id=id))
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.restaurant = restaurant
            reservation.user = request.user
            reservation.save()
            return render(request, 'reservation_confirmation.html', {'msg': f"Table booked in {reservation.restaurant} on {reservation.date} at {reservation.time_from}", 'restaurant': restaurant})
        return render(request, 'reservation_form.html', {'form': form, 'restaurant': restaurant})


class EditReservationView(LoginRequiredMixin, View):
    def get(self, request, id):
        reservation = Reservation.objects.get(pk=id)
        ReservationForm.base_fields['table'] = forms.ModelChoiceField(
            queryset=Table.objects.filter(restaurant_id=reservation.restaurant_id))
        form = ReservationForm(instance=reservation)
        return render(request, 'reservation_edit_form.html', {'form': form})

    def post(self, request, id):
        reservation = Reservation.objects.get(pk=id)
        form = ReservationForm(request.POST, instance=reservation)
        reservation.delete()
        if form.is_valid():
            rsrv = form.save(commit=False)
            rsrv.restaurant = reservation.restaurant
            rsrv.user = request.user
            rsrv.save()
            return redirect('my_account')
        return render(request, 'reservation_edit_form.html', {'form': form})


class DeleteReservationView(LoginRequiredMixin, View):
    def get(self, request, id):
        reservation = Reservation.objects.get(id=id)
        return render(request, 'reservation_delete.html', {'object': f'reservation for {reservation}'})

    def post(self, request, id):
        if request.POST.get('answer') == "Yes":
            rsrv = Reservation.objects.get(id=id)
            rsrv.delete()
            return redirect('my_account')
        return redirect('my_account')


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
        restaurants = Restaurant.objects.all().order_by('name')
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
        return render(request, 'admin_form.html', {'form': form})

    def post(self, request):
        restaurants = Restaurant.objects.all().order_by('name')
        form = RestaurantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'admin_restaurants.html', {'restaurants': restaurants})
        return render(request, 'admin_form.html', {'form': form})


class EditRestaurantView(PermissionRequiredMixin, UpdateView):
    permission_required = ['click_and_table.change_restaurant']

    model = Restaurant
    fields = '__all__'
    success_url = reverse_lazy('admin_restaurants')
    template_name = 'admin_form.html'


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
        return render(request, 'admin_form.html', {'form': form})

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
    template_name = 'admin_form.html'


class DeleteCategoryView(PermissionRequiredMixin, View):
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
        return render(request, 'admin_form.html', {'form': form})

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
    template_name = 'admin_form.html'


class DeleteCityView(PermissionRequiredMixin, View):
    permission_required = ['click_and_table.delete_city']

    def get(self, request, id):
        city = City.objects.get(id=id)
        return render(request, 'admin_delete.html', {'object': city})

    def post(self, request, id):
        cities = City.objects.all()
        if request.POST.get('answer') == "Yes":
            city = City.objects.get(id=id)
            city.delete()
            return render(request, 'admin_cities.html', {'cities': cities})
        return render(request, 'admin_cities.html', {'cities': cities})


class AddTableView(PermissionRequiredMixin, View):
    permission_required = ['click_and_table.add_table']

    def get(self, request, rest_id):
        form = TableForm(initial={'restaurant': rest_id})
        return render(request, 'admin_form.html', {'form': form})

    def post(self, request, rest_id):
        restaurant = Restaurant.objects.get(pk=rest_id)
        tables = Table.objects.filter(restaurant_id=rest_id)
        form = TableForm(request.POST)
        if form.is_valid():
            table = form.save(commit=False)
            table.restaurant_id = rest_id
            table.save()
        return render(request, 'admin_tables.html', {'tables': tables, 'restaurant': restaurant})


class EditTableView(PermissionRequiredMixin, UpdateView):
    permission_required = ['click_and_table.change_table']

    model = Table
    fields = '__all__'
    template_name = 'admin_form.html'


class DeleteTableView(PermissionRequiredMixin, View):
    permission_required = ['click_and_table.delete_table']

    def get(self, request, table_id):
        table = Table.objects.get(id=table_id)
        return render(request, 'admin_delete.html', {'object': table})

    def post(self, request, table_id):
        tables = Table.objects.filter(id=table_id)
        if request.POST.get('answer') == "Yes":
            table = Table.objects.get(id=table_id)
            table.delete()
            return redirect('admin_tables', id=table.restaurant.id)
        restaurant = Restaurant.objects.get(pk=id)
        return render(request, 'admin_tables.html', {'tables': tables, 'restaurant': restaurant})
