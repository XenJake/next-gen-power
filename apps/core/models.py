from django.db import models


class ContactMessage(models.Model):
	class InquiryType(models.TextChoices):
		CUSTOMER = 'customer', 'Vehicle or charging enquiry'
		PARTNERSHIP = 'partnership', 'Business partnership'
		SITE = 'site', 'Charging site or property'
		OTHER = 'other', 'Other'

	name = models.CharField(max_length=120)
	email = models.EmailField()
	phone = models.CharField(max_length=40, blank=True)
	inquiry_type = models.CharField(max_length=20, choices=InquiryType.choices, default=InquiryType.CUSTOMER)
	subject = models.CharField(max_length=160, blank=True)
	message = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	is_handled = models.BooleanField(default=False)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return f'{self.name}: {self.subject or "Contact request"}'
