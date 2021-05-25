from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError

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

    def clean(self):
        data = super().clean()
        date_str = datetime.strptime(str(data['date']), '%Y-%m-%d').date()
        today = datetime.now().date()
        table = data['table']
        date = data['date']
        time_from = data['time_from']
        time_to = data['time_to']

        check_1 = Reservation.objects.filter(table_id=table, date=date, time_from__lte=time_from,
                                             time_to__gte=time_from).exists()
        check_2 = Reservation.objects.filter(table_id=table, date=date, time_from__lte=time_to,
                                             time_to__gte=time_to).exists()
        check_3 = Reservation.objects.filter(table_id=table, date=date, time_from__gte=time_from,
                                             time_to__lte=time_to).exists()
        if check_1 or check_2 or check_3:
            raise ValidationError('Table not available in the requested time. Please choose another table and/or time')
        elif date_str <= today:
            raise ValidationError('Booking must be done at least one day in advance')
        else:
            return data