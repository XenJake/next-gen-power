from django.contrib import admin

from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
	list_display = ['name', 'email', 'inquiry_type', 'subject', 'is_handled', 'created_at']
	list_filter = ['inquiry_type', 'is_handled', 'created_at']
	search_fields = ['name', 'email', 'subject', 'message']
	readonly_fields = ['created_at']
