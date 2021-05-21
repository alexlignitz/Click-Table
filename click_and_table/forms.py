from django import forms

from click_and_table.models import Restaurant, Category, City, Table, Reservation


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


class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = '__all__'


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['table', 'date', 'time_from', 'time_to']
        widgets = {
            'date': DateInput,
            'time_from': TimeInput,
            'time_to': TimeInput
        }
