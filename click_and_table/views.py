from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView

from click_and_table.forms import RestaurantForm, CategoryForm, CityForm
from click_and_table.models import Category, City, Restaurant


class Indexview(View):
    def get(self, request):
        return render(request, '__base__.html')


class RestaurantListView(View):
    def get(self, request):
        restaurants = Restaurant.objects.all()
        return render(request, 'restaurant_list.html', {'restaurants': restaurants})


class RestaurantDetailsView(View):
    def get(self, request):
        return render(request, 'restaurant_details.html')


class ContactView(View):
    def get(self, request):
        return render(request, 'contact_us.html')


class HelpView(View):
    def get(self, request):
        return render(request, 'help.html')


# ------------------------------------- LOGIN REQUIRED -------------------------------------------------------------

class VotingView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'voting.html')


# ------------------------------------- ADMIN TOOLS -------------------------------------------------------------

class AdminView(PermissionRequiredMixin, View):
    permission_required = ['click_and_table.change_restaurant', 'click_and_table.add_restaurant',
                           'click_and_table.delete_restaurant', 'click_and_table.change_category',
                           'click_and_table.add_category', 'click_and_table.delete_category',
                           'click_and_table.change_city', 'click_and_table.add_city', 'click_and_table.delete_city']

    def get(self, request):
        return render(request, 'admin_tools.html')


class AdminRestaurantsView(View):
    permission_required = ['click_and_table.change_restaurant', 'click_and_table.add_restaurant',
                           'click_and_table.delete_restaurant', 'click_and_table.change_category',
                           'click_and_table.add_category', 'click_and_table.delete_category',
                           'click_and_table.change_city', 'click_and_table.add_city', 'click_and_table.delete_city']

    def get(self, request):
        restaurants = Restaurant.objects.all()
        return render(request, 'admin_restaurants.html', {'restaurants': restaurants})


class AdminCategoriesView(View):
    permission_required = ['click_and_table.change_restaurant', 'click_and_table.add_restaurant',
                           'click_and_table.delete_restaurant', 'click_and_table.change_category',
                           'click_and_table.add_category', 'click_and_table.delete_category',
                           'click_and_table.change_city', 'click_and_table.add_city', 'click_and_table.delete_city']

    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'admin_categories.html', {'categories': categories})


class AdminCitiesView(View):
    permission_required = ['click_and_table.change_restaurant', 'click_and_table.add_restaurant',
                           'click_and_table.delete_restaurant', 'click_and_table.change_category',
                           'click_and_table.add_category', 'click_and_table.delete_category',
                           'click_and_table.change_city', 'click_and_table.add_city', 'click_and_table.delete_city']

    def get(self, request):
        cities = City.objects.all()
        return render(request, 'admin_cities.html', {'cities': cities})


class AddRestaurantView(PermissionRequiredMixin, View):
    permission_required = ['click_and_table.add_restaurant']

    def get(self, request):
        form = RestaurantForm
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = RestaurantForm(request.POST)
        if form.is_valid():
            form.save()
        return render(request, 'message_template.html', {'msg': 'Restaurant added'})


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
        if request.POST.get('answer') == "Yes":
            restaurant = Restaurant.objects.get(id=id)
            restaurant.delete()
            return render(request, 'message_template.html', {'msg': 'Restaurant deleted'})
        restaurants = Restaurant.objects.all()
        return render(request, 'admin_restaurants.html', {'restaurants': restaurants})


class AddCategoryView(PermissionRequiredMixin, View):
    permission_required = ['click_and_table.add_category']

    def get(self, request):
        form = CategoryForm
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            Category.objects.create(name=name)
        return render(request, 'message_template.html', {'msg': 'Category created'})


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
        if request.POST.get('answer') == "Yes":
            category = Category.objects.get(id=id)
            category.delete()
            return render(request, 'message_template.html', {'msg': 'Category deleted'})
        categories = Category.objects.all()
        return render(request, 'admin_categories.html', {'categories': categories})


class AddCityView(PermissionRequiredMixin, View):
    permission_required = ['click_and_table.add_city']

    def get(self, request):
        form = CityForm
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = CityForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            City.objects.create(name=name)
        return render(request, 'message_template.html', {'msg': 'City added'})


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
        if request.POST.get('answer') == "Yes":
            city = City.objects.get(id=id)
            city.delete()
            return render(request, 'message_template.html', {'msg': 'City deleted'})
        cities = City.objects.all()
        return render(request, 'admin_cities.html', {'cities': cities})