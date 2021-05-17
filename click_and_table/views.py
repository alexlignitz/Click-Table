from django.shortcuts import render

# Create your views here.
from django.views import View


class Indexview(View):
    def get(self, request):
        return render(request, '__base__.html')


class VotingView(View):
    def get(self, request):
        return render(request, 'voting.html')


class RestaurantListView(View):
    def get(self, request):
        return render(request, 'restaurant_list.html')


class RestaurantDetailsView(View):
    def get(self, request):
        return render(request, 'restaurant_details.html')
