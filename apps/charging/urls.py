from django.urls import path

from . import views

app_name = 'charging'

urlpatterns = [
    path('how-it-works/', views.how_it_works, name='how_it_works'),
    path('', views.station_list, name='station_list'),
    path('stations/<slug:slug>/', views.station_detail, name='station_detail'),
    path('chargers/<uuid:public_id>/', views.charger_qr, name='charger_qr'),
    path('chargers/<uuid:public_id>/qr.svg', views.charger_qr_svg, name='charger_qr_svg'),
    path('chargers/<uuid:public_id>/start/', views.start_session, name='start_session'),
    path('api/v1/stations/', views.station_api, name='station_api'),
    path('api/v1/chargers/<uuid:public_id>/', views.charger_api, name='charger_api'),
]
