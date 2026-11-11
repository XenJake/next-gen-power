from django.contrib import admin

from .models import Manufacturer, Vehicle, VehicleEnquiry, VehicleImage


class VehicleImageInline(admin.TabularInline):
	model = VehicleImage
	extra = 0
	fields = ['image', 'image_url', 'local_path', 'alt_text', 'position', 'credit', 'license_name', 'license_url', 'source_url']


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
	search_fields = ['name', 'country']


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
	list_display = ['manufacturer', 'model_name', 'trim', 'body_style', 'availability', 'price', 'is_demo', 'is_published']
	list_filter = ['manufacturer', 'availability', 'is_demo', 'is_published', 'is_featured']
	search_fields = ['manufacturer__name', 'model_name', 'trim']
	prepopulated_fields = {'slug': ['model_name']}
	inlines = [VehicleImageInline]
	fieldsets = [
		(None, {'fields': ['manufacturer', 'model_name', 'trim', 'slug', 'model_year', 'body_style', 'description']}),
		('Pricing and supplier-confirmed inclusions', {
			'fields': ['price', 'currency', 'included_accessories', 'availability'],
		}),
		('Specifications', {
			'fields': ['range_km', 'battery_kwh', 'max_charging_kw', 'connector_type', 'power_kw', 'seating'],
		}),
		('Publication', {'fields': ['is_featured', 'is_published', 'is_demo']}),
	]


@admin.register(VehicleEnquiry)
class VehicleEnquiryAdmin(admin.ModelAdmin):
	list_display = ['name', 'vehicle', 'email', 'status', 'created_at']
	list_filter = ['status', 'created_at']
	search_fields = ['name', 'email', 'phone', 'message']
	readonly_fields = ['created_at']
