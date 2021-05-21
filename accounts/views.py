from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from click_and_table.models import Reservation


class RegistrationView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/login.html'


class MyAccountView(LoginRequiredMixin, View):
    def get(self, request):
        reservations = Reservation.objects.filter(user=request.user).order_by('date')
        return render(request, 'my_account.html', {'reservations': reservations})

