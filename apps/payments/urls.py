from django.urls import path

from . import commerce_views, views

app_name = 'payments'

urlpatterns = [
    path('chargers/', commerce_views.charger_store, name='charger_store'),
    path('orders/vehicle/<slug:slug>/', commerce_views.start_vehicle_order, name='start_vehicle_order'),
    path('orders/<uuid:public_id>/checkout/', commerce_views.order_checkout, name='order_checkout'),
    path('orders/<uuid:public_id>/mock/', commerce_views.mock_order_checkout, name='mock_order_checkout'),
    path('<uuid:public_id>/checkout/', views.checkout, name='checkout'),
    path('<uuid:public_id>/mock/', views.mock_checkout, name='mock_checkout'),
    path('webhook/', views.webhook, name='webhook'),
]
