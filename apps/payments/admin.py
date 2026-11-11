from django.contrib import admin

from .models import ChargerProduct, Payment, SeasonalDeal, VehicleOrder


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
	list_display = ['public_id', 'session', 'method', 'amount', 'currency', 'status', 'created_at']
	list_filter = ['status', 'method', 'provider', 'created_at']
	search_fields = ['public_id', 'provider_reference', 'session__public_id']
	readonly_fields = [
		'session', 'public_id', 'provider', 'provider_reference', 'idempotency_key',
		'method', 'amount', 'currency', 'status', 'created_at', 'updated_at',
	]

	def has_add_permission(self, request):
		return False

	def has_delete_permission(self, request, obj=None):
		return False


@admin.register(ChargerProduct)
class ChargerProductAdmin(admin.ModelAdmin):
	list_display = ['name', 'product_type', 'price', 'currency', 'is_published']
	list_filter = ['product_type', 'currency', 'is_published']
	search_fields = ['name', 'description']


@admin.register(SeasonalDeal)
class SeasonalDealAdmin(admin.ModelAdmin):
	list_display = ['name', 'discount_percent', 'starts_at', 'ends_at', 'is_active']
	list_filter = ['is_active', 'starts_at', 'ends_at']
	search_fields = ['name', 'description']
	date_hierarchy = 'starts_at'


@admin.register(VehicleOrder)
class VehicleOrderAdmin(admin.ModelAdmin):
	list_display = ['public_id', 'vehicle_name', 'charger_name', 'amount', 'currency', 'method', 'status', 'created_at']
	list_filter = ['status', 'method', 'created_at']
	search_fields = ['public_id', 'vehicle_name', 'charger_name', 'customer_name', 'customer_email', 'customer_phone']
	readonly_fields = [field.name for field in VehicleOrder._meta.fields]

	def has_add_permission(self, request):
		return False

	def has_delete_permission(self, request, obj=None):
		return False
