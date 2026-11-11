from django import forms
from django.contrib.auth import get_user_model

from apps.charging.models import Charger, ChargingStation
from apps.operations.models import FaultReport, MaintenanceRecord
from apps.vehicles.models import Vehicle, VehicleImage


class VehicleOperationsForm(forms.ModelForm):
    image = forms.ImageField(required=False, help_text='Optional main vehicle photograph.')

    class Meta:
        model = Vehicle
        fields = [
            'manufacturer', 'model_name', 'trim', 'slug', 'model_year', 'body_style',
            'description', 'price', 'currency', 'availability', 'range_km',
            'battery_kwh', 'max_charging_kw', 'connector_type', 'power_kw',
            'seating', 'is_featured', 'is_demo', 'is_published',
        ]

    def save(self, commit=True):
        vehicle = super().save(commit=commit)
        image = self.cleaned_data.get('image')
        if commit and image:
            VehicleImage.objects.update_or_create(
                vehicle=vehicle,
                position=0,
                defaults={'image': image, 'alt_text': f'{vehicle} vehicle photograph'},
            )
        return vehicle


class StationOperationsForm(forms.ModelForm):
    class Meta:
        model = ChargingStation
        fields = [
            'name', 'slug', 'site_type', 'address', 'city', 'region', 'latitude',
            'longitude', 'opening_hours', 'amenities', 'status', 'solar_capacity_kw',
            'battery_storage_kwh', 'is_demo', 'is_published',
        ]
        widgets = {'amenities': forms.Textarea(attrs={'rows': 3})}


class ChargerOperationsForm(forms.ModelForm):
    class Meta:
        model = Charger
        fields = [
            'station', 'charger_code', 'power_type', 'connector_type', 'max_power_kw',
            'status', 'is_demo', 'external_reference',
        ]


class FaultOperationsForm(forms.ModelForm):
    class Meta:
        model = FaultReport
        fields = ['station', 'charger', 'title', 'description', 'severity', 'status']
        widgets = {'description': forms.Textarea(attrs={'rows': 4})}


class MaintenanceOperationsForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRecord
        fields = ['station', 'charger', 'assigned_to', 'title', 'notes', 'scheduled_for', 'status', 'completed_at']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
            'scheduled_for': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'completed_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = get_user_model().objects.filter(is_active=True, is_staff=True).order_by('username')
