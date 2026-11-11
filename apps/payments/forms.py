from django import forms

from .models import ChargerProduct, Payment


PAYMENT_METHOD_CHOICES = [
    (Payment.Method.MTN_MOMO, 'MTN Mobile Money'),
    (Payment.Method.TELECEL_CASH, 'Telecel Cash'),
    (Payment.Method.AT_MONEY, 'AT Money'),
    (Payment.Method.VISA, 'Visa'),
    (Payment.Method.MASTERCARD, 'Mastercard'),
]


class CheckoutMethodForm(forms.Form):
    method = forms.ChoiceField(
        choices=PAYMENT_METHOD_CHOICES,
        widget=forms.RadioSelect,
        label='Choose how to pay',
    )


class CustomerDetailsForm(forms.Form):
    customer_name = forms.CharField(
        max_length=120,
        label='Full name',
        widget=forms.TextInput(attrs={'autocomplete': 'name'}),
    )
    customer_email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'autocomplete': 'email'}),
    )
    customer_phone = forms.CharField(
        max_length=40,
        label='Phone',
        widget=forms.TextInput(attrs={'autocomplete': 'tel'}),
    )


class VehiclePurchaseForm(CustomerDetailsForm):
    charger_product = forms.ModelChoiceField(
        queryset=ChargerProduct.objects.none(),
        required=False,
        empty_label='Vehicle only',
        label='Add a home charger',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['charger_product'].queryset = ChargerProduct.objects.filter(is_published=True)


class ChargerPurchaseForm(CustomerDetailsForm):
    charger_product = forms.ModelChoiceField(
        queryset=ChargerProduct.objects.none(),
        label='Choose a home charger',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['charger_product'].queryset = ChargerProduct.objects.filter(is_published=True)
