from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import VehicleEnquiryForm
from .models import Manufacturer, Vehicle


def catalogue(request):
	vehicles = Vehicle.objects.filter(is_published=True).select_related('manufacturer').prefetch_related('images')
	query = request.GET.get('q', '').strip()
	manufacturer = request.GET.get('manufacturer', '').strip()
	body_style = request.GET.get('type', '').strip()
	if query:
		vehicles = vehicles.filter(Q(model_name__icontains=query) | Q(trim__icontains=query) | Q(manufacturer__name__icontains=query))
	if manufacturer:
		vehicles = vehicles.filter(manufacturer__name__iexact=manufacturer)
	if body_style in Vehicle.BodyStyle.values:
		vehicles = vehicles.filter(body_style=body_style)
	manufacturers = Manufacturer.objects.filter(vehicles__is_published=True).distinct().order_by('name')
	return render(request, 'vehicles/catalogue.html', {
		'vehicles': vehicles,
		'manufacturers': manufacturers,
		'body_styles': Vehicle.BodyStyle.choices,
		'query': query,
		'selected_manufacturer': manufacturer,
		'selected_body_style': body_style,
	})


def detail(request, slug):
	vehicle = get_object_or_404(
		Vehicle.objects.select_related('manufacturer').prefetch_related('images'),
		slug=slug,
		is_published=True,
	)
	form = VehicleEnquiryForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		enquiry = form.save(commit=False)
		enquiry.vehicle = vehicle
		enquiry.save()
		messages.success(request, 'Your vehicle enquiry has been sent to our team.')
		return redirect(vehicle.get_absolute_url())
	return render(request, 'vehicles/detail.html', {'vehicle': vehicle, 'form': form})
