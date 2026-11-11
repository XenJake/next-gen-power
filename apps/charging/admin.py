from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Charger, ChargingSession, ChargingStation


class ChargerInline(admin.TabularInline):
	model = Charger
	extra = 0
	readonly_fields = ['public_id', 'last_heartbeat_at']


@admin.register(ChargingStation)
class ChargingStationAdmin(admin.ModelAdmin):
	list_display = ['name', 'city', 'region', 'status', 'is_demo', 'is_published']
	list_filter = ['status', 'city', 'is_demo', 'is_published']
	search_fields = ['name', 'address', 'city', 'region']
	prepopulated_fields = {'slug': ['name']}
	inlines = [ChargerInline]


@admin.register(Charger)
class ChargerAdmin(admin.ModelAdmin):
	list_display = ['charger_code', 'station', 'connector_type', 'max_power_kw', 'status', 'is_demo', 'last_heartbeat_at', 'qr_links']
	list_filter = ['status', 'connector_type', 'is_demo', 'station__city']
	search_fields = ['charger_code', 'external_reference', 'station__name']
	readonly_fields = ['public_id', 'last_heartbeat_at']

	@admin.display(description='QR')
	def qr_links(self, obj):
		page = reverse('charging:charger_qr', kwargs={'public_id': obj.public_id})
		image = reverse('charging:charger_qr_svg', kwargs={'public_id': obj.public_id})
		return format_html('<a href="{}">Open charger</a> · <a href="{}">QR image</a>', page, image)


@admin.register(ChargingSession)
class ChargingSessionAdmin(admin.ModelAdmin):
	list_display = ['public_id', 'charger', 'status', 'amount', 'currency', 'created_at']
	list_filter = ['status', 'currency', 'created_at']
	search_fields = ['public_id', 'external_session_id', 'charger__charger_code']
	readonly_fields = ['public_id', 'status', 'created_at', 'updated_at']
