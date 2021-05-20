import django_filters
from django_filters import CharFilter, ModelMultipleChoiceFilter

from django import forms
from .models import *


class RestaurantFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', label='Restaurant name:', lookup_expr='icontains')
    category = ModelMultipleChoiceFilter(field_name='category', queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Restaurant
        fields = ['name', 'category', 'city']

