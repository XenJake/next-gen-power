import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


class ChargingStation(models.Model):
	class SiteType(models.TextChoices):
		MALL = 'mall', 'Shopping mall'
		HOTEL = 'hotel', 'Hotel'
		OFFICE = 'office', 'Office building'
		HIGHWAY = 'highway', 'Highway charging hub'
		OTHER = 'other', 'Other'

	class Status(models.TextChoices):
		OPERATIONAL = 'operational', 'Operational'
		LIMITED = 'limited', 'Limited service'
		CLOSED = 'closed', 'Temporarily closed'

	name = models.CharField(max_length=160)
	slug = models.SlugField(unique=True)
	address = models.CharField(max_length=240)
	site_type = models.CharField(max_length=16, choices=SiteType.choices, default=SiteType.OTHER)
	city = models.CharField(max_length=100)
	region = models.CharField(max_length=100, blank=True)
	latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
	longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
	opening_hours = models.CharField(max_length=160, blank=True)
	amenities = models.TextField(blank=True)
	status = models.CharField(max_length=16, choices=Status.choices, default=Status.OPERATIONAL)
	is_demo = models.BooleanField(default=False, help_text='Demonstration location; not a live operating station.')
	solar_capacity_kw = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
	battery_storage_kwh = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
	is_published = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['city', 'name']
		indexes = [models.Index(fields=['is_published', 'city'])]

	def __str__(self):
		return f'{self.name} ({self.city})'

	def get_absolute_url(self):
		return reverse('charging:station_detail', kwargs={'slug': self.slug})


class Charger(models.Model):
	class PowerType(models.TextChoices):
		AC = 'ac', 'AC'
		DC = 'dc', 'DC'

	class Status(models.TextChoices):
		AVAILABLE = 'available', 'Available'
		IN_USE = 'in_use', 'Occupied'
		FAULTED = 'faulted', 'Faulted'
		MAINTENANCE = 'maintenance', 'Maintenance'
		OFFLINE = 'offline', 'Offline'
		OUT_OF_SERVICE = 'out_of_service', 'Out of service'

	station = models.ForeignKey(ChargingStation, on_delete=models.PROTECT, related_name='chargers')
	public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
	charger_code = models.CharField(max_length=80)
	power_type = models.CharField(max_length=2, choices=PowerType.choices, default=PowerType.AC)
	connector_type = models.CharField(max_length=80)
	max_power_kw = models.DecimalField(max_digits=7, decimal_places=2)
	status = models.CharField(max_length=16, choices=Status.choices, default=Status.OFFLINE)
	is_demo = models.BooleanField(default=False, help_text='Demonstration charger status; not a live status feed.')
	external_reference = models.CharField(max_length=120, blank=True)
	last_heartbeat_at = models.DateTimeField(null=True, blank=True)

	class Meta:
		ordering = ['station__name', 'charger_code']
		constraints = [models.UniqueConstraint(fields=['station', 'charger_code'], name='unique_charger_code_per_station')]
		indexes = [models.Index(fields=['status', 'station'])]

	def __str__(self):
		return f'{self.station.name} - {self.charger_code}'

	def get_qr_url(self):
		return reverse('charging:charger_qr', kwargs={'public_id': self.public_id})


class ChargingSession(models.Model):
	class Status(models.TextChoices):
		PENDING_PAYMENT = 'pending_payment', 'Awaiting payment'
		PAID_PENDING_AUTH = 'paid_pending_auth', 'Paid, awaiting charger authorization'
		AUTHORIZED = 'authorized', 'Authorized'
		CHARGING = 'charging', 'Charging'
		COMPLETED = 'completed', 'Completed'
		FAILED = 'failed', 'Failed'
		CANCELLED = 'cancelled', 'Cancelled'

	public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
	charger = models.ForeignKey(Charger, on_delete=models.PROTECT, related_name='sessions')
	customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='charging_sessions')
	external_session_id = models.CharField(max_length=120, blank=True)
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING_PAYMENT)
	energy_kwh = models.DecimalField(max_digits=9, decimal_places=3, null=True, blank=True)
	amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
	currency = models.CharField(max_length=3, default='GHS')
	started_at = models.DateTimeField(null=True, blank=True)
	ended_at = models.DateTimeField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-created_at']
		indexes = [models.Index(fields=['status', 'created_at'])]

	def __str__(self):
		return f'{self.public_id} - {self.get_status_display()}'

	def clean(self):
		if self.status in {self.Status.AUTHORIZED, self.Status.CHARGING} and not self.pk:
			raise ValidationError('A charging session can only be authorized after payment confirmation.')
