from django.urls import path

from . import views

app_name = 'operations'

urlpatterns = [
    path('', views.OperationsDashboardView.as_view(), name='dashboard'),
    path('vehicles/', views.VehicleListView.as_view(), name='vehicles'),
    path('vehicles/new/', views.VehicleCreateView.as_view(), name='vehicle_create'),
    path('vehicles/<int:pk>/edit/', views.VehicleUpdateView.as_view(), name='vehicle_edit'),
    path('stations/', views.StationListView.as_view(), name='stations'),
    path('stations/new/', views.StationCreateView.as_view(), name='station_create'),
    path('stations/<int:pk>/edit/', views.StationUpdateView.as_view(), name='station_edit'),
    path('chargers/', views.ChargerListView.as_view(), name='chargers'),
    path('chargers/new/', views.ChargerCreateView.as_view(), name='charger_create'),
    path('chargers/<int:pk>/edit/', views.ChargerUpdateView.as_view(), name='charger_edit'),
    path('sessions/', views.SessionListView.as_view(), name='sessions'),
    path('payments/', views.PaymentListView.as_view(), name='payments'),
    path('enquiries/', views.EnquiryListView.as_view(), name='enquiries'),
    path('faults/', views.FaultListView.as_view(), name='faults'),
    path('faults/new/', views.FaultCreateView.as_view(), name='fault_create'),
    path('faults/<int:pk>/edit/', views.FaultUpdateView.as_view(), name='fault_edit'),
    path('maintenance/', views.MaintenanceListView.as_view(), name='maintenance'),
    path('maintenance/new/', views.MaintenanceCreateView.as_view(), name='maintenance_create'),
    path('maintenance/<int:pk>/edit/', views.MaintenanceUpdateView.as_view(), name='maintenance_edit'),
]
