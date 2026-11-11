from django import forms

from .models import ChargingSession


class StartChargingForm(forms.Form):
    amount = forms.DecimalField(min_value=1, max_value=5000, decimal_places=2, max_digits=7, label='Prepaid amount (GHS)')
    method = forms.ChoiceField(
        choices=[('mobile_money', 'Mobile money'), ('card', 'Card')],
        label='Payment method',
    )
