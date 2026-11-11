from django.db import models
from django.urls import reverse


class Manufacturer(models.Model):
	name = models.CharField(max_length=120, unique=True)
	country = models.CharField(max_length=80, blank=True)
	website = models.URLField(blank=True)

	class Meta:
		ordering = ['name']

	def __str__(self):
		return self.name


class Vehicle(models.Model):
	class Availability(models.TextChoices):
		AVAILABLE = 'available', 'Available'
		INCOMING = 'incoming', 'Incoming'
		ENQUIRE = 'enquire', 'Enquire for availability'
		SOLD = 'sold', 'Sold'

	class BodyStyle(models.TextChoices):
		SUV = 'SUV', 'SUV'
		SEDAN = 'Sedan', 'Sedan'
		HATCHBACK = 'Hatchback', 'Hatchback'
		PICKUP = 'Pickup', 'Pickup'

	manufacturer = models.ForeignKey(Manufacturer, on_delete=models.PROTECT, related_name='vehicles')
	model_name = models.CharField(max_length=120)
	trim = models.CharField(max_length=120, blank=True)
	slug = models.SlugField(unique=True)
	model_year = models.PositiveSmallIntegerField(null=True, blank=True)
	body_style = models.CharField(max_length=80, choices=BodyStyle.choices, blank=True)
	description = models.TextField()
	price = models.DecimalField(max_digits=13, decimal_places=2, null=True, blank=True)
	currency = models.CharField(max_length=3, default='GHS')
	availability = models.CharField(max_length=16, choices=Availability.choices, default=Availability.ENQUIRE)
	range_km = models.PositiveIntegerField(null=True, blank=True)
	battery_kwh = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
	max_charging_kw = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
	connector_type = models.CharField(max_length=80, blank=True)
	power_kw = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
	seating = models.PositiveSmallIntegerField(null=True, blank=True)
	is_featured = models.BooleanField(default=False)
	is_published = models.BooleanField(default=False)
	is_demo = models.BooleanField(default=False, help_text='Demo listing. Prices and specifications are illustrative, not a quotation.')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['manufacturer__name', 'model_name', 'trim']
		indexes = [models.Index(fields=['is_published', 'is_featured'])]

	def __str__(self):
		label = f'{self.manufacturer.name} {self.model_name}'
		return f'{label} {self.trim}'.strip()

	def get_absolute_url(self):
		return reverse('vehicles:detail', kwargs={'slug': self.slug})


class VehicleImage(models.Model):
	vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='images')
	image = models.ImageField(upload_to='vehicles/')
	alt_text = models.CharField(max_length=180)
	position = models.PositiveSmallIntegerField(default=0)

	class Meta:
		ordering = ['position', 'id']

	def __str__(self):
		return f'Image for {self.vehicle}'


class VehicleEnquiry(models.Model):
	class Status(models.TextChoices):
		NEW = 'new', 'New'
		CONTACTED = 'contacted', 'Contacted'
		CLOSED = 'closed', 'Closed'

	vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True, related_name='enquiries')
	name = models.CharField(max_length=120)
	email = models.EmailField()
	phone = models.CharField(max_length=40)
	message = models.TextField(blank=True)
	status = models.CharField(max_length=16, choices=Status.choices, default=Status.NEW)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return f'{self.name} - {self.vehicle or "General vehicle enquiry"}'
