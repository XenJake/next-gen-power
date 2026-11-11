from decimal import Decimal, ROUND_HALF_UP

from django.conf import settings
from django.utils import timezone

from .models import ChargerProduct, SeasonalDeal

CENT = Decimal('0.01')
ZERO = Decimal('0.00')


def money(value):
	return Decimal(value).quantize(CENT, rounding=ROUND_HALF_UP)


def vehicle_price_in_ghs(vehicle):
	if vehicle.price is None:
		return None
	if vehicle.currency == 'USD':
		return money(vehicle.price * Decimal(str(settings.USD_GHS_EXCHANGE_RATE)))
	if vehicle.currency == 'GHS':
		return money(vehicle.price)
	return None


def active_seasonal_deal(at=None):
	at = at or timezone.now()
	return SeasonalDeal.objects.filter(
		is_active=True,
		starts_at__lte=at,
		ends_at__gt=at,
	).order_by('-discount_percent', '-starts_at').first()


def build_order_quote(vehicle=None, charger_product=None, deal=None):
	vehicle_amount = vehicle_price_in_ghs(vehicle) if vehicle else ZERO
	if vehicle and vehicle_amount is None:
		raise ValueError('This vehicle does not have a supported purchase price.')

	charger_amount = money(charger_product.price) if charger_product else ZERO
	if charger_product and charger_product.currency != 'GHS':
		raise ValueError('Home charger products must be priced in GHS.')

	seasonal_discount_percent = deal.discount_percent if vehicle and deal else ZERO
	seasonal_discount = money(vehicle_amount * seasonal_discount_percent / Decimal('100'))
	after_seasonal = vehicle_amount - seasonal_discount
	bundle_discount_percent = (
		Decimal(str(settings.BUNDLE_DISCOUNT_PERCENT))
		if vehicle and charger_product
		else ZERO
	)
	bundle_discount = money((after_seasonal + charger_amount) * bundle_discount_percent / Decimal('100'))
	amount = money(after_seasonal + charger_amount - bundle_discount)

	return {
		'vehicle_amount': vehicle_amount,
		'charger_amount': charger_amount,
		'seasonal_deal': deal if seasonal_discount_percent else None,
		'seasonal_deal_name': deal.name if seasonal_discount_percent else '',
		'seasonal_discount_percent': seasonal_discount_percent,
		'seasonal_discount': seasonal_discount,
		'bundle_discount_percent': bundle_discount_percent,
		'bundle_discount': bundle_discount,
		'amount': amount,
	}


def published_chargers():
	return ChargerProduct.objects.filter(is_published=True)
