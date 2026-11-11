from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class FaultReport(models.Model):
	class Severity(models.TextChoices):
		LOW = 'low', 'Low'
		MEDIUM = 'medium', 'Medium'
		HIGH = 'high', 'High'
		CRITICAL = 'critical', 'Critical'

	class Status(models.TextChoices):
		OPEN = 'open', 'Open'
		INVESTIGATING = 'investigating', 'Investigating'
		RESOLVED = 'resolved', 'Resolved'

	station = models.ForeignKey('charging.ChargingStation', on_delete=models.PROTECT, null=True, blank=True, related_name='fault_reports')
	charger = models.ForeignKey('charging.Charger', on_delete=models.PROTECT, null=True, blank=True, related_name='fault_reports')
	reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
	title = models.CharField(max_length=160)
	description = models.TextField()
	severity = models.CharField(max_length=12, choices=Severity.choices, default=Severity.MEDIUM)
	status = models.CharField(max_length=16, choices=Status.choices, default=Status.OPEN)
	created_at = models.DateTimeField(auto_now_add=True)
	resolved_at = models.DateTimeField(null=True, blank=True)

	class Meta:
		ordering = ['-created_at']

	def clean(self):
		if not self.station_id and not self.charger_id:
			raise ValidationError('A fault must be linked to a station or charger.')
		if self.charger_id and self.station_id and self.charger.station_id != self.station_id:
			raise ValidationError('The selected charger must belong to the selected station.')

	def __str__(self):
		return self.title


class MaintenanceRecord(models.Model):
	class Status(models.TextChoices):
		SCHEDULED = 'scheduled', 'Scheduled'
		IN_PROGRESS = 'in_progress', 'In progress'
		COMPLETED = 'completed', 'Completed'
		CANCELLED = 'cancelled', 'Cancelled'

	station = models.ForeignKey('charging.ChargingStation', on_delete=models.PROTECT, related_name='maintenance_records')
	charger = models.ForeignKey('charging.Charger', on_delete=models.PROTECT, null=True, blank=True, related_name='maintenance_records')
	assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
	title = models.CharField(max_length=160)
	notes = models.TextField(blank=True)
	scheduled_for = models.DateTimeField()
	completed_at = models.DateTimeField(null=True, blank=True)
	status = models.CharField(max_length=16, choices=Status.choices, default=Status.SCHEDULED)

	class Meta:
		ordering = ['scheduled_for']

	def clean(self):
		if self.charger_id and self.station_id and self.charger.station_id != self.station_id:
			raise ValidationError('The selected charger must belong to the selected station.')

	def __str__(self):
		return self.title
