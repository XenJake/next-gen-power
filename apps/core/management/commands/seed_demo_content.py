from decimal import Decimal

from django.core.management.base import BaseCommand

from apps.charging.models import Charger, ChargingStation
from apps.vehicles.models import Manufacturer, Vehicle


class Command(BaseCommand):
    help = 'Load clearly labeled illustrative BYD catalogue entries and demo charging sites.'

    def handle(self, *args, **options):
        byd, _ = Manufacturer.objects.update_or_create(
            name='BYD', defaults={'country': 'China', 'website': 'https://www.byd.com/'}
        )
        vehicles = [
            {
                'model_name': 'Seal', 'trim': 'Premium AWD', 'slug': 'byd-seal-premium-awd',
                'model_year': 2025, 'body_style': Vehicle.BodyStyle.SEDAN,
                'description': 'Demonstration catalogue entry for the BYD Seal Premium AWD. Confirm exact specifications and market availability with our team.',
                'price': Decimal('689000'), 'range_km': 570, 'battery_kwh': Decimal('82.5'),
                'max_charging_kw': Decimal('150'), 'connector_type': 'CCS2', 'power_kw': Decimal('390'),
                'seating': 5,
            },
            {
                'model_name': 'Atto 3', 'trim': 'Extended Range', 'slug': 'byd-atto-3-extended-range',
                'model_year': 2025, 'body_style': Vehicle.BodyStyle.SUV,
                'description': 'Demonstration catalogue entry for the BYD Atto 3 Extended Range. Confirm exact specifications and market availability with our team.',
                'price': Decimal('429000'), 'range_km': 420, 'battery_kwh': Decimal('60.5'),
                'max_charging_kw': Decimal('88'), 'connector_type': 'CCS2', 'power_kw': Decimal('150'),
                'seating': 5,
            },
            {
                'model_name': 'Dolphin', 'trim': 'Premium', 'slug': 'byd-dolphin-premium',
                'model_year': 2025, 'body_style': Vehicle.BodyStyle.HATCHBACK,
                'description': 'Demonstration catalogue entry for the BYD Dolphin Premium. Confirm exact specifications and market availability with our team.',
                'price': Decimal('329000'), 'range_km': 427, 'battery_kwh': Decimal('60.4'),
                'max_charging_kw': Decimal('80'), 'connector_type': 'CCS2', 'power_kw': Decimal('150'),
                'seating': 5,
            },
        ]
        for index, values in enumerate(vehicles):
            Vehicle.objects.update_or_create(
                slug=values['slug'],
                defaults={
                    **values,
                    'manufacturer': byd,
                    'currency': 'GHS',
                    'availability': Vehicle.Availability.ENQUIRE,
                    'is_featured': index < 3,
                    'is_published': True,
                    'is_demo': True,
                },
            )

        station_data = [
            ('Demo Accra Central', 'demo-accra-central', 'Demonstration coordinates near Accra Central', 'Accra', 'Greater Accra', Decimal('5.6037'), Decimal('-0.1870'), 'DEMO-AC-01', 'CCS2', Decimal('120'), Charger.Status.AVAILABLE),
            ('Demo Tema Roadside', 'demo-tema-roadside', 'Demonstration coordinates near Tema', 'Tema', 'Greater Accra', Decimal('5.6698'), Decimal('0.0166'), 'DEMO-TE-01', 'CCS2', Decimal('180'), Charger.Status.IN_USE),
            ('Demo Kumasi Hub', 'demo-kumasi-hub', 'Demonstration coordinates near Kumasi', 'Kumasi', 'Ashanti', Decimal('6.6885'), Decimal('-1.6244'), 'DEMO-KU-01', 'CCS2', Decimal('120'), Charger.Status.OFFLINE),
            ('Demo Cape Coast Point', 'demo-cape-coast-point', 'Demonstration coordinates near Cape Coast', 'Cape Coast', 'Central', Decimal('5.1053'), Decimal('-1.2466'), 'DEMO-CC-01', 'Type 2', Decimal('22'), Charger.Status.OUT_OF_SERVICE),
        ]
        for name, slug, address, city, region, latitude, longitude, code, connector, power, status in station_data:
            station, _ = ChargingStation.objects.update_or_create(
                slug=slug,
                defaults={
                    'name': name,
                    'address': address,
                    'city': city,
                    'region': region,
                    'latitude': latitude,
                    'longitude': longitude,
                    'opening_hours': 'Illustrative hours: 06:00-22:00',
                    'amenities': 'Demonstration content. This is not a live operating station.',
                    'status': ChargingStation.Status.OPERATIONAL,
                    'is_published': True,
                    'is_demo': True,
                },
            )
            Charger.objects.update_or_create(
                station=station,
                charger_code=code,
                defaults={
                    'connector_type': connector,
                    'max_power_kw': power,
                    'status': status,
                    'is_demo': True,
                },
            )

        self.stdout.write(self.style.SUCCESS('Loaded 3 illustrative BYD listings and 4 demonstration charging sites.'))
        self.stdout.write('Demo prices, specifications, coordinates and charger statuses are illustrative only.')
