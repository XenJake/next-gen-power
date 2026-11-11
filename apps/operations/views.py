from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render

from apps.charging.models import Charger, ChargingSession, ChargingStation
from apps.operations.models import FaultReport, MaintenanceRecord
from apps.payments.models import Payment


@login_required
def dashboard(request):
	if not request.user.is_active or not request.user.is_staff or not request.user.has_perm('charging.view_chargingsession'):
		return HttpResponseForbidden('You do not have permission to access operations.')
	context = {
		'station_count': ChargingStation.objects.count(),
		'charger_count': Charger.objects.count(),
		'available_chargers': Charger.objects.filter(status=Charger.Status.AVAILABLE).count(),
		'active_sessions': ChargingSession.objects.filter(status__in=[ChargingSession.Status.AUTHORIZED, ChargingSession.Status.CHARGING]).count(),
		'authorization_pending': ChargingSession.objects.filter(status=ChargingSession.Status.PAID_PENDING_AUTH).count(),
		'pending_payments': Payment.objects.filter(status=Payment.Status.PENDING).count(),
		'open_faults': FaultReport.objects.exclude(status=FaultReport.Status.RESOLVED).select_related('station', 'charger')[:8],
		'upcoming_maintenance': MaintenanceRecord.objects.filter(status__in=[MaintenanceRecord.Status.SCHEDULED, MaintenanceRecord.Status.IN_PROGRESS]).select_related('station', 'charger')[:8],
		'recent_sessions': ChargingSession.objects.select_related('charger__station').order_by('-created_at')[:8],
	}
	return render(request, 'operations/dashboard.html', context)
