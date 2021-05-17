from django import forms

from click_and_table.models import Restaurant, Category, City


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(),
            'category': forms.CheckboxSelectMultiple
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = '__all__'
