from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from apps.payments.forms import VehiclePurchaseForm
from apps.payments.pricing import active_seasonal_deal, build_order_quote, vehicle_price_in_ghs

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
	active_deal = active_seasonal_deal()
	for vehicle in vehicles:
		vehicle.purchase_price_ghs = vehicle_price_in_ghs(vehicle)
		vehicle.purchase_quote = (
			build_order_quote(vehicle=vehicle, deal=active_deal)
			if vehicle.purchase_price_ghs is not None
			else None
		)
	return render(request, 'vehicles/catalogue.html', {
		'vehicles': vehicles,
		'manufacturers': manufacturers,
		'body_styles': Vehicle.BodyStyle.choices,
		'query': query,
		'selected_manufacturer': manufacturer,
		'selected_body_style': body_style,
		'active_deal': active_deal,
		'exchange_rate': settings.USD_GHS_EXCHANGE_RATE,
		'rate_as_of': settings.USD_GHS_RATE_AS_OF,
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
	deal = active_seasonal_deal()
	price_ghs = vehicle_price_in_ghs(vehicle)
	return render(request, 'vehicles/detail.html', {
		'vehicle': vehicle,
		'form': form,
		'purchase_form': VehiclePurchaseForm(),
		'quote': build_order_quote(vehicle=vehicle, deal=deal) if price_ghs is not None else None,
		'active_deal': deal,
		'exchange_rate': settings.USD_GHS_EXCHANGE_RATE,
		'rate_as_of': settings.USD_GHS_RATE_AS_OF,
		'price_ghs': price_ghs,
	})
