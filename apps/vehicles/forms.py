from django import forms

from .models import VehicleEnquiry


class VehicleEnquiryForm(forms.ModelForm):
    class Meta:
        model = VehicleEnquiry
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }
