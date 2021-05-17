from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View


class Indexview(View):
    def get(self, request):
        return render(request, '__base__.html')


class VotingView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'voting.html')


class RestaurantListView(View):
    def get(self, request):
        return render(request, 'restaurant_list.html')


class RestaurantDetailsView(View):
    def get(self, request):
        return render(request, 'restaurant_details.html')


class ContactView(View):
    def get(self, request):
        return render(request, 'contact_us.html')