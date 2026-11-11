from django.contrib import messages
from django.shortcuts import redirect, render

from apps.vehicles.models import Vehicle

from .forms import ContactMessageForm


def home(request):
	featured_vehicles = Vehicle.objects.filter(is_published=True, is_featured=True).prefetch_related('images')[:3]
	return render(request, 'core/home.html', {'featured_vehicles': featured_vehicles})


def about(request):
	return render(request, 'core/about.html')


def sustainability(request):
	return render(request, 'core/sustainability.html')


def contact(request):
	form = ContactMessageForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		form.save()
		messages.success(request, 'Thank you. Your message has been received.')
		return redirect('core:contact')
	return render(request, 'core/contact.html', {'form': form})
