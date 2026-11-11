from django.contrib import admin

from .models import FaultReport, MaintenanceRecord


@admin.register(FaultReport)
class FaultReportAdmin(admin.ModelAdmin):
	list_display = ['title', 'station', 'charger', 'severity', 'status', 'created_at']
	list_filter = ['severity', 'status', 'created_at']
	search_fields = ['title', 'description', 'station__name', 'charger__charger_code']
	readonly_fields = ['created_at']


@admin.register(MaintenanceRecord)
class MaintenanceRecordAdmin(admin.ModelAdmin):
	list_display = ['title', 'station', 'charger', 'scheduled_for', 'status']
	list_filter = ['status', 'scheduled_for']
	search_fields = ['title', 'notes', 'station__name', 'charger__charger_code']
