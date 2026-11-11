import json
from io import BytesIO

import qrcode
from qrcode.image.svg import SvgPathImage
from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.payments.models import Payment

from .forms import StartChargingForm
from .models import Charger, ChargingSession, ChargingStation
from .serializers import ChargerStatusSerializer, StationSerializer


def how_it_works(request):
	return render(request, 'charging/how_it_works.html')


def station_list(request):
	stations = ChargingStation.objects.filter(is_published=True).prefetch_related('chargers')
	query = request.GET.get('q', '').strip()
	city = request.GET.get('city', '').strip()
	status = request.GET.get('status', '').strip()
	site_type = request.GET.get('site_type', '').strip()
	if query:
		stations = stations.filter(Q(name__icontains=query) | Q(city__icontains=query) | Q(region__icontains=query))
	if city:
		stations = stations.filter(city__iexact=city)
	if status in Charger.Status.values:
		stations = stations.filter(chargers__status=status).distinct()
	if site_type in ChargingStation.SiteType.values:
		stations = stations.filter(site_type=site_type)
	map_data = []
	for station in stations:
		chargers = list(station.chargers.all())
		if station.latitude is None or station.longitude is None:
			continue
		map_data.append({
			'name': station.name,
			'site_type': station.get_site_type_display(),
			'city': station.city,
			'address': station.address,
			'latitude': float(station.latitude),
			'longitude': float(station.longitude),
			'url': station.get_absolute_url(),
			'is_demo': station.is_demo,
			'available': sum(charger.status == Charger.Status.AVAILABLE for charger in chargers),
			'charger_count': len(chargers),
			'statuses': [charger.get_status_display() for charger in chargers],
			'equipment': [f'{charger.max_power_kw:g} kW {charger.get_power_type_display()} / {charger.connector_type}' for charger in chargers],
		})
	all_stations = ChargingStation.objects.filter(is_published=True)
	return render(request, 'charging/station_list.html', {
		'stations': stations,
		'query': query,
		'cities': all_stations.values_list('city', flat=True).distinct().order_by('city'),
		'selected_city': city,
		'selected_status': status,
		'site_types': ChargingStation.SiteType.choices,
		'selected_site_type': site_type,
		'charger_statuses': Charger.Status.choices,
		'map_data': map_data,
	})


def station_detail(request, slug):
	station = get_object_or_404(ChargingStation.objects.prefetch_related('chargers'), slug=slug, is_published=True)
	return render(request, 'charging/station_detail.html', {'station': station})


def charger_qr(request, public_id):
	charger = get_object_or_404(Charger.objects.select_related('station'), public_id=public_id, station__is_published=True)
	provider_configured = bool(settings.PAYMENT_PROVIDER_CLASS)
	form = StartChargingForm() if provider_configured else None
	has_pending_session = charger.sessions.filter(status__in=[
		ChargingSession.Status.PAID_PENDING_AUTH,
		ChargingSession.Status.AUTHORIZED,
		ChargingSession.Status.CHARGING,
	]).exists()
	return render(request, 'charging/charger.html', {
		'charger': charger,
		'form': form,
		'provider_configured': provider_configured,
		'has_pending_session': has_pending_session,
	})


def charger_qr_svg(request, public_id):
	get_object_or_404(Charger, public_id=public_id, station__is_published=True)
	target_url = request.build_absolute_uri(reverse('charging:charger_qr', kwargs={'public_id': public_id}))
	code = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=8, border=4, image_factory=SvgPathImage)
	code.add_data(target_url)
	image = code.make_image()
	output = BytesIO()
	image.save(output)
	return HttpResponse(output.getvalue(), content_type='image/svg+xml', headers={'Cache-Control': 'public, max-age=300'})


def start_session(request, public_id):
	if request.method != 'POST':
		return redirect('charging:charger_qr', public_id=public_id)
	charger = get_object_or_404(Charger.objects.select_related('station'), public_id=public_id, station__is_published=True)
	if not settings.PAYMENT_PROVIDER_CLASS:
		messages.error(request, 'Online charging payments are not enabled. No payment or charging session was created.')
		return redirect('charging:charger_qr', public_id=public_id)
	form = StartChargingForm(request.POST)
	if not form.is_valid():
		return render(request, 'charging/charger.html', {'charger': charger, 'form': form, 'has_pending_session': False})
	with transaction.atomic():
		locked_charger = Charger.objects.select_for_update().get(pk=charger.pk)
		active_statuses = [
			ChargingSession.Status.PAID_PENDING_AUTH,
			ChargingSession.Status.AUTHORIZED,
			ChargingSession.Status.CHARGING,
		]
		if locked_charger.status != Charger.Status.AVAILABLE or locked_charger.sessions.filter(status__in=active_statuses).exists():
			messages.error(request, 'This charger is not available to start a new session.')
			return redirect('charging:charger_qr', public_id=public_id)
		amount = form.cleaned_data['amount']
		session = ChargingSession.objects.create(
			charger=locked_charger,
			amount=amount,
			currency='GHS',
			status=ChargingSession.Status.PENDING_PAYMENT,
		)
		Payment.objects.create(
			session=session,
			method=form.cleaned_data['method'],
			amount=amount,
			currency='GHS',
		)
	return redirect('payments:checkout', public_id=session.payments.first().public_id)


@api_view(['GET'])
@permission_classes([AllowAny])
def station_api(request):
	stations = ChargingStation.objects.filter(is_published=True).prefetch_related('chargers')
	return Response(StationSerializer(stations, many=True).data)


@api_view(['GET'])
@permission_classes([AllowAny])
def charger_api(request, public_id):
	charger = get_object_or_404(Charger.objects.select_related('station'), public_id=public_id, station__is_published=True)
	return Response(ChargerStatusSerializer(charger).data)
