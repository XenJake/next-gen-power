import uuid
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q


class Payment(models.Model):
	class Status(models.TextChoices):
		PENDING = 'pending', 'Pending'
		SUCCEEDED = 'succeeded', 'Succeeded'
		FAILED = 'failed', 'Failed'
		REFUNDED = 'refunded', 'Refunded'

	class Method(models.TextChoices):
		MTN_MOMO = 'mtn_momo', 'MTN Mobile Money'
		TELECEL_CASH = 'telecel_cash', 'Telecel Cash'
		AT_MONEY = 'at_money', 'AT Money'
		VISA = 'visa', 'Visa'
		MASTERCARD = 'mastercard', 'Mastercard'
		MOBILE_MONEY = 'mobile_money', 'Mobile money'
		CARD = 'card', 'Card'

	session = models.ForeignKey('charging.ChargingSession', on_delete=models.PROTECT, related_name='payments')
	public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
	provider = models.CharField(max_length=60, blank=True)
	provider_reference = models.CharField(max_length=160, blank=True)
	idempotency_key = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
	method = models.CharField(max_length=20, choices=Method.choices, blank=True, default='')
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	currency = models.CharField(max_length=3, default='GHS')
	status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-created_at']
		indexes = [models.Index(fields=['status', 'created_at'])]

	def __str__(self):
		return f'{self.public_id} - {self.get_status_display()}'


class ChargerProduct(models.Model):
	class ProductType(models.TextChoices):
		STANDARD = 'standard', 'Standard Home Charger'
		PREMIUM = 'premium', 'Premium Home Charger'

	product_type = models.CharField(max_length=16, choices=ProductType.choices, unique=True)
	name = models.CharField(max_length=120)
	description = models.TextField()
	price = models.DecimalField(
		max_digits=10,
		decimal_places=2,
		default=Decimal('0.00'),
		validators=[MinValueValidator(Decimal('0.00'))],
	)
	currency = models.CharField(max_length=3, default='GHS')
	is_published = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['price', 'name']

	def __str__(self):
		return self.name

	def clean(self):
		super().clean()
		if self.price < Decimal('0.00'):
			raise ValidationError({'price': 'The product price cannot be negative.'})


class SeasonalDeal(models.Model):
	name = models.CharField(max_length=120)
	description = models.TextField(blank=True)
	discount_percent = models.DecimalField(
		max_digits=5,
		decimal_places=2,
		validators=[MinValueValidator(Decimal('0.01')), MaxValueValidator(Decimal('100.00'))],
	)
	starts_at = models.DateTimeField()
	ends_at = models.DateTimeField()
	is_active = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-starts_at']
		constraints = [
			models.CheckConstraint(
				condition=Q(ends_at__gt=models.F('starts_at')),
				name='seasonal_deal_end_after_start',
			),
		]

	def clean(self):
		super().clean()
		if self.starts_at and self.ends_at and self.ends_at <= self.starts_at:
			raise ValidationError({'ends_at': 'The deal end must be after its start.'})

	def __str__(self):
		return self.name


class VehicleOrder(models.Model):
	class Status(models.TextChoices):
		PENDING = 'pending', 'Awaiting mock payment'
		MOCK_PAID = 'mock_paid', 'Mock payment recorded'

	public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
	vehicle = models.ForeignKey(
		'vehicles.Vehicle',
		on_delete=models.PROTECT,
		null=True,
		blank=True,
		related_name='commerce_orders',
	)
	charger_product = models.ForeignKey(
		ChargerProduct,
		on_delete=models.PROTECT,
		null=True,
		blank=True,
		related_name='commerce_orders',
	)
	vehicle_name = models.CharField(max_length=240, blank=True)
	charger_name = models.CharField(max_length=120, blank=True)
	customer_name = models.CharField(max_length=120)
	customer_email = models.EmailField()
	customer_phone = models.CharField(max_length=40)
	vehicle_amount = models.DecimalField(max_digits=13, decimal_places=2, default=Decimal('0.00'))
	charger_amount = models.DecimalField(max_digits=13, decimal_places=2, default=Decimal('0.00'))
	seasonal_deal = models.ForeignKey(
		SeasonalDeal,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name='orders',
	)
	seasonal_deal_name = models.CharField(max_length=120, blank=True)
	seasonal_discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
	seasonal_discount = models.DecimalField(max_digits=13, decimal_places=2, default=Decimal('0.00'))
	bundle_discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
	bundle_discount = models.DecimalField(max_digits=13, decimal_places=2, default=Decimal('0.00'))
	amount = models.DecimalField(max_digits=13, decimal_places=2)
	currency = models.CharField(max_length=3, default='GHS')
	method = models.CharField(max_length=20, choices=Payment.Method.choices, blank=True, default='')
	status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)
	mock_reference = models.CharField(max_length=40, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	paid_at = models.DateTimeField(null=True, blank=True)

	class Meta:
		ordering = ['-created_at']
		indexes = [models.Index(fields=['status', 'created_at'])]
		constraints = [
			models.CheckConstraint(
				condition=Q(vehicle__isnull=False) | Q(charger_product__isnull=False),
				name='commerce_order_has_a_product',
			),
		]

	def clean(self):
		super().clean()
		if not self.vehicle and not self.charger_product:
			raise ValidationError('An order must include a vehicle, a charger, or both.')

	def __str__(self):
		return f'{self.public_id} - {self.get_status_display()}'
