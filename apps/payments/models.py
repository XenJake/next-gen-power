import uuid

from django.db import models


class Payment(models.Model):
	class Status(models.TextChoices):
		PENDING = 'pending', 'Pending'
		SUCCEEDED = 'succeeded', 'Succeeded'
		FAILED = 'failed', 'Failed'
		REFUNDED = 'refunded', 'Refunded'

	class Method(models.TextChoices):
		MOBILE_MONEY = 'mobile_money', 'Mobile money'
		CARD = 'card', 'Card'

	session = models.ForeignKey('charging.ChargingSession', on_delete=models.PROTECT, related_name='payments')
	public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
	provider = models.CharField(max_length=60, blank=True)
	provider_reference = models.CharField(max_length=160, blank=True)
	idempotency_key = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
	method = models.CharField(max_length=20, choices=Method.choices)
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
