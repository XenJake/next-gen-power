from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView, TemplateView, UpdateView

from apps.charging.models import Charger, ChargingSession, ChargingStation
from apps.operations.models import FaultReport, MaintenanceRecord
from apps.payments.models import Payment
from apps.vehicles.models import Vehicle, VehicleEnquiry

from .forms import (
	ChargerOperationsForm,
	FaultOperationsForm,
	MaintenanceOperationsForm,
	StationOperationsForm,
	VehicleOperationsForm,
)


class OperationsPermissionMixin(LoginRequiredMixin, PermissionRequiredMixin):
	raise_exception = False

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated and (not request.user.is_active or not request.user.is_staff):
			return HttpResponseForbidden('Staff access is required for operations.')
		return super().dispatch(request, *args, **kwargs)

	def handle_no_permission(self):
		if self.request.user.is_authenticated:
			return HttpResponseForbidden('You do not have permission to access this operations section.')
		return super().handle_no_permission()


class OperationsDashboardView(OperationsPermissionMixin, TemplateView):
	template_name = 'operations/dashboard.html'
	permission_required = (
		'charging.view_chargingstation',
		'charging.view_charger',
		'charging.view_chargingsession',
		'payments.view_payment',
	)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context.update({
			'section': 'overview',
			'station_count': ChargingStation.objects.count(),
			'charger_count': Charger.objects.count(),
			'available_chargers': Charger.objects.filter(status=Charger.Status.AVAILABLE).count(),
			'active_sessions': ChargingSession.objects.filter(status__in=[ChargingSession.Status.AUTHORIZED, ChargingSession.Status.CHARGING]).count(),
			'authorization_pending': ChargingSession.objects.filter(status=ChargingSession.Status.PAID_PENDING_AUTH).count(),
			'pending_payments': Payment.objects.filter(status=Payment.Status.PENDING).count(),
			'open_faults': FaultReport.objects.exclude(status=FaultReport.Status.RESOLVED).select_related('station', 'charger')[:6],
			'upcoming_maintenance': MaintenanceRecord.objects.filter(status__in=[MaintenanceRecord.Status.SCHEDULED, MaintenanceRecord.Status.IN_PROGRESS]).select_related('station', 'charger')[:6],
			'recent_sessions': ChargingSession.objects.select_related('charger__station').order_by('-created_at')[:8],
		})
		return context


class OperationsListView(OperationsPermissionMixin, ListView):
	template_name = 'operations/resource_list.html'
	context_object_name = 'items'
	paginate_by = 30
	section = ''
	page_title = ''
	page_description = ''
	create_url_name = ''
	create_permission = ''
	list_url_name = ''
	filter_key = 'status'
	status_choices = ()
	permission_required = ()

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context.update({
			'section': self.section,
			'page_title': self.page_title,
			'page_description': self.page_description,
			'create_url_name': self.create_url_name,
			'list_url_name': self.list_url_name,
			'filter_key': self.filter_key,
			'selected_filter': self.request.GET.get(self.filter_key, ''),
			'status_choices': self.status_choices,
			'can_create': bool(self.create_permission and (self.request.user.is_superuser or self.request.user.has_perm(self.create_permission))),
			'can_change': self.request.user.is_superuser or self.request.user.has_perm(
				f'{self.model._meta.app_label}.change_{self.model._meta.model_name}'
			),
		})
		return context


class VehicleListView(OperationsListView):
	model = Vehicle
	section = 'vehicles'
	page_title = 'Vehicle inventory'
	page_description = 'Manage sourced vehicles, verified specifications, prices and publication status.'
	create_url_name = 'operations:vehicle_create'
	create_permission = 'vehicles.add_vehicle'
	list_url_name = 'operations:vehicles'
	permission_required = 'vehicles.view_vehicle'

	def get_queryset(self):
		queryset = Vehicle.objects.select_related('manufacturer')
		query = self.request.GET.get('q', '').strip()
		if query:
			queryset = queryset.filter(Q(model_name__icontains=query) | Q(manufacturer__name__icontains=query) | Q(trim__icontains=query))
		return queryset


class StationListView(OperationsListView):
	model = ChargingStation
	section = 'stations'
	page_title = 'Charging locations'
	page_description = 'Manage malls, hotels, offices and highway hubs across the network.'
	create_url_name = 'operations:station_create'
	create_permission = 'charging.add_chargingstation'
	list_url_name = 'operations:stations'
	filter_key = 'site_type'
	status_choices = ChargingStation.SiteType.choices
	permission_required = 'charging.view_chargingstation'

	def get_queryset(self):
		queryset = ChargingStation.objects.prefetch_related('chargers')
		query = self.request.GET.get('q', '').strip()
		site_type = self.request.GET.get('site_type', '').strip()
		if query:
			queryset = queryset.filter(Q(name__icontains=query) | Q(city__icontains=query) | Q(address__icontains=query))
		if site_type in ChargingStation.SiteType.values:
			queryset = queryset.filter(site_type=site_type)
		return queryset


class ChargerListView(OperationsListView):
	model = Charger
	section = 'chargers'
	page_title = 'Charger fleet'
	page_description = 'Review connector, AC/DC type, rated power, availability and QR entry for each unit.'
	create_url_name = 'operations:charger_create'
	create_permission = 'charging.add_charger'
	list_url_name = 'operations:chargers'
	list_url_name = 'operations:chargers'
	status_choices = Charger.Status.choices
	permission_required = 'charging.view_charger'

	def get_queryset(self):
		queryset = Charger.objects.select_related('station')
		query = self.request.GET.get('q', '').strip()
		status = self.request.GET.get('status', '').strip()
		if query:
			queryset = queryset.filter(Q(charger_code__icontains=query) | Q(station__name__icontains=query) | Q(connector_type__icontains=query) | Q(external_reference__icontains=query))
		if status in Charger.Status.values:
			queryset = queryset.filter(status=status)
		return queryset


class SessionListView(OperationsListView):
	model = ChargingSession
	section = 'sessions'
	page_title = 'Charging sessions'
	page_description = 'Monitor session state, energy delivered, customer charges and controller status.'
	permission_required = 'charging.view_chargingsession'
	list_url_name = 'operations:sessions'
	status_choices = ChargingSession.Status.choices

	def get_queryset(self):
		queryset = ChargingSession.objects.select_related('charger__station', 'customer')
		status = self.request.GET.get('status', '').strip()
		query = self.request.GET.get('q', '').strip()
		if status in ChargingSession.Status.values:
			queryset = queryset.filter(status=status)
		if query:
			queryset = queryset.filter(Q(public_id__icontains=query) | Q(charger__charger_code__icontains=query) | Q(charger__station__name__icontains=query))
		return queryset


class PaymentListView(OperationsListView):
	model = Payment
	section = 'payments'
	page_title = 'Payments'
	page_description = 'Review payment references and settlement status. Payment records are read-only for auditability.'
	permission_required = 'payments.view_payment'
	list_url_name = 'operations:payments'
	status_choices = Payment.Status.choices

	def get_queryset(self):
		queryset = Payment.objects.select_related('session__charger__station')
		status = self.request.GET.get('status', '').strip()
		query = self.request.GET.get('q', '').strip()
		if status in Payment.Status.values:
			queryset = queryset.filter(status=status)
		if query:
			queryset = queryset.filter(Q(provider_reference__icontains=query) | Q(session__public_id__icontains=query) | Q(session__charger__station__name__icontains=query))
		return queryset


class EnquiryListView(OperationsListView):
	model = VehicleEnquiry
	section = 'enquiries'
	page_title = 'Vehicle enquiries'
	page_description = 'Follow up with customers interested in sourced inventory.'
	permission_required = 'vehicles.view_vehicleenquiry'
	list_url_name = 'operations:enquiries'

	def get_queryset(self):
		queryset = VehicleEnquiry.objects.select_related('vehicle', 'vehicle__manufacturer')
		query = self.request.GET.get('q', '').strip()
		if query:
			queryset = queryset.filter(Q(name__icontains=query) | Q(email__icontains=query) | Q(phone__icontains=query))
		return queryset


class FaultListView(OperationsListView):
	model = FaultReport
	section = 'faults'
	page_title = 'Fault reports'
	page_description = 'Triage network issues by severity and track resolution.'
	create_url_name = 'operations:fault_create'
	create_permission = 'operations.add_faultreport'
	list_url_name = 'operations:faults'
	status_choices = FaultReport.Status.choices
	permission_required = 'operations.view_faultreport'

	def get_queryset(self):
		queryset = FaultReport.objects.select_related('station', 'charger', 'reported_by')
		status = self.request.GET.get('status', '').strip()
		query = self.request.GET.get('q', '').strip()
		if status in FaultReport.Status.values:
			queryset = queryset.filter(status=status)
		if query:
			queryset = queryset.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(station__name__icontains=query))
		return queryset


class MaintenanceListView(OperationsListView):
	model = MaintenanceRecord
	section = 'maintenance'
	page_title = 'Maintenance planner'
	page_description = 'Schedule station and charger maintenance and track work in progress.'
	create_url_name = 'operations:maintenance_create'
	create_permission = 'operations.add_maintenancerecord'
	list_url_name = 'operations:maintenance'
	status_choices = MaintenanceRecord.Status.choices
	permission_required = 'operations.view_maintenancerecord'

	def get_queryset(self):
		queryset = MaintenanceRecord.objects.select_related('station', 'charger', 'assigned_to')
		query = self.request.GET.get('q', '').strip()
		status = self.request.GET.get('status', '').strip()
		if query:
			queryset = queryset.filter(Q(title__icontains=query) | Q(station__name__icontains=query) | Q(charger__charger_code__icontains=query))
		if status in MaintenanceRecord.Status.values:
			queryset = queryset.filter(status=status)
		return queryset


class OperationsCreateView(OperationsPermissionMixin, SuccessMessageMixin, CreateView):
	template_name = 'operations/resource_form.html'
	page_title = ''
	section = ''
	success_message = 'Record created.'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context.update({'page_title': self.page_title, 'section': self.section, 'is_edit': False})
		return context


class OperationsUpdateView(OperationsPermissionMixin, SuccessMessageMixin, UpdateView):
	template_name = 'operations/resource_form.html'
	page_title = ''
	section = ''
	success_message = 'Changes saved.'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context.update({'page_title': self.page_title, 'section': self.section, 'is_edit': True})
		return context


class VehicleCreateView(OperationsCreateView):
	model = Vehicle
	form_class = VehicleOperationsForm
	page_title = 'Add a sourced vehicle'
	section = 'vehicles'
	permission_required = 'vehicles.add_vehicle'
	success_url = reverse_lazy('operations:vehicles')


class VehicleUpdateView(OperationsUpdateView):
	model = Vehicle
	form_class = VehicleOperationsForm
	page_title = 'Edit vehicle listing'
	section = 'vehicles'
	permission_required = 'vehicles.change_vehicle'
	success_url = reverse_lazy('operations:vehicles')


class StationCreateView(OperationsCreateView):
	model = ChargingStation
	form_class = StationOperationsForm
	page_title = 'Add a charging location'
	section = 'stations'
	permission_required = 'charging.add_chargingstation'
	success_url = reverse_lazy('operations:stations')


class StationUpdateView(OperationsUpdateView):
	model = ChargingStation
	form_class = StationOperationsForm
	page_title = 'Edit charging location'
	section = 'stations'
	permission_required = 'charging.change_chargingstation'
	success_url = reverse_lazy('operations:stations')


class ChargerCreateView(OperationsCreateView):
	model = Charger
	form_class = ChargerOperationsForm
	page_title = 'Add a charger'
	section = 'chargers'
	permission_required = 'charging.add_charger'
	success_url = reverse_lazy('operations:chargers')


class ChargerUpdateView(OperationsUpdateView):
	model = Charger
	form_class = ChargerOperationsForm
	page_title = 'Edit charger'
	section = 'chargers'
	permission_required = 'charging.change_charger'
	success_url = reverse_lazy('operations:chargers')


class FaultCreateView(OperationsCreateView):
	model = FaultReport
	form_class = FaultOperationsForm
	page_title = 'Report a network fault'
	section = 'faults'
	permission_required = 'operations.add_faultreport'
	success_url = reverse_lazy('operations:faults')

	def form_valid(self, form):
		form.instance.reported_by = self.request.user
		if form.instance.status == FaultReport.Status.RESOLVED and not form.instance.resolved_at:
			form.instance.resolved_at = timezone.now()
		return super().form_valid(form)


class FaultUpdateView(OperationsUpdateView):
	model = FaultReport
	form_class = FaultOperationsForm
	page_title = 'Update fault report'
	section = 'faults'
	permission_required = 'operations.change_faultreport'
	success_url = reverse_lazy('operations:faults')

	def form_valid(self, form):
		if form.instance.status == FaultReport.Status.RESOLVED:
			form.instance.resolved_at = form.instance.resolved_at or timezone.now()
		else:
			form.instance.resolved_at = None
		return super().form_valid(form)


class MaintenanceCreateView(OperationsCreateView):
	model = MaintenanceRecord
	form_class = MaintenanceOperationsForm
	page_title = 'Schedule maintenance'
	section = 'maintenance'
	permission_required = 'operations.add_maintenancerecord'
	success_url = reverse_lazy('operations:maintenance')


class MaintenanceUpdateView(OperationsUpdateView):
	model = MaintenanceRecord
	form_class = MaintenanceOperationsForm
	page_title = 'Update maintenance record'
	section = 'maintenance'
	permission_required = 'operations.change_maintenancerecord'
	success_url = reverse_lazy('operations:maintenance')
