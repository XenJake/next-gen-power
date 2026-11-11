from django.contrib import admin

from .models import Payment


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
