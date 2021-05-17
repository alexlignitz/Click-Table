from django.urls import path, include
from accounts.views import RegistrationView, MyAccountView

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('my_account', MyAccountView.as_view(), name="my_account"),
]