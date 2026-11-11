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

        mall_hotel_office_sites = [
            {
                'name': 'Demo Accra Mall', 'slug': 'demo-accra-mall',
                'address': 'Tetteh Quarshie Road, Accra', 'city': 'Accra', 'region': 'Greater Accra',
                'site_type': ChargingStation.SiteType.MALL,
                'latitude': Decimal('5.6221843'), 'longitude': Decimal('-0.1729361'),
            },
            {
                'name': 'Demo West Hills Mall', 'slug': 'demo-west-hills-mall',
                'address': 'New Weija, Ga South, Greater Accra', 'city': 'Accra', 'region': 'Greater Accra',
                'site_type': ChargingStation.SiteType.MALL,
                'latitude': Decimal('5.5447144'), 'longitude': Decimal('-0.3438056'),
            },
            {
                'name': 'Demo Atlantic Mall', 'slug': 'demo-atlantic-mall',
                'address': 'Kofi Annan East Avenue, North Legon, Accra', 'city': 'Accra', 'region': 'Greater Accra',
                'site_type': ChargingStation.SiteType.MALL,
                'latitude': Decimal('5.6679935'), 'longitude': Decimal('-0.1781440'),
            },
            {
                'name': 'Demo Labadi Beach Hotel', 'slug': 'demo-labadi-beach-hotel',
                'address': 'La Road, La, Accra', 'city': 'Accra', 'region': 'Greater Accra',
                'site_type': ChargingStation.SiteType.HOTEL,
                'latitude': Decimal('5.5639522'), 'longitude': Decimal('-0.1380137'),
            },
            {
                'name': 'Demo One Airport Square', 'slug': 'demo-one-airport-square',
                'address': 'South Liberation Link, Airport City, Accra', 'city': 'Accra', 'region': 'Greater Accra',
                'site_type': ChargingStation.SiteType.OFFICE,
                'latitude': Decimal('5.6007783'), 'longitude': Decimal('-0.1772592'),
            },
        ]
        highway_sites = [
            {
                'name': 'Demo Accra-Kumasi Highway Hub - Suhum', 'slug': 'demo-accra-kumasi-suhum',
                'address': 'Demonstration service area near Suhum on the Accra-Kumasi corridor',
                'city': 'Suhum', 'region': 'Eastern', 'site_type': ChargingStation.SiteType.HIGHWAY,
                'latitude': Decimal('6.0358850'), 'longitude': Decimal('-0.4552751'), 'dc_chargers': 3,
            },
            {
                'name': 'Demo Accra-Cape Coast Highway Hub - Winneba', 'slug': 'demo-accra-cape-coast-winneba',
                'address': 'Demonstration service area near Winneba on the Accra-Cape Coast corridor',
                'city': 'Winneba', 'region': 'Central', 'site_type': ChargingStation.SiteType.HIGHWAY,
                'latitude': Decimal('5.3500600'), 'longitude': Decimal('-0.6213400'), 'dc_chargers': 2,
            },
        ]
        status_cycle = [
            Charger.Status.AVAILABLE,
            Charger.Status.AVAILABLE,
            Charger.Status.IN_USE,
            Charger.Status.OFFLINE,
            Charger.Status.OUT_OF_SERVICE,
            Charger.Status.MAINTENANCE,
            Charger.Status.AVAILABLE,
            Charger.Status.IN_USE,
            Charger.Status.FAULTED,
            Charger.Status.AVAILABLE,
        ]
        for site in [*mall_hotel_office_sites, *highway_sites]:
            is_highway = site['site_type'] == ChargingStation.SiteType.HIGHWAY
            station, _ = ChargingStation.objects.update_or_create(
                slug=site['slug'],
                defaults={
                    'name': site['name'],
                    'address': site['address'],
                    'site_type': site['site_type'],
                    'city': site['city'],
                    'region': site['region'],
                    'latitude': site['latitude'],
                    'longitude': site['longitude'],
                    'opening_hours': 'Illustrative host-site hours; confirm with the property.' if not is_highway else 'Illustrative 24-hour service area; not an operating site.',
                    'amenities': 'Demonstration location only. No NEXT GEN POWER charging equipment is deployed here.',
                    'status': ChargingStation.Status.OPERATIONAL,
                    'is_published': True,
                    'is_demo': True,
                },
            )
            charger_total = site.get('dc_chargers', 0) if is_highway else 10
            for index in range(charger_total):
                power_type = Charger.PowerType.DC if is_highway else Charger.PowerType.AC
                charger_number = index + 1
                Charger.objects.update_or_create(
                    station=station,
                    charger_code=f'{"DC" if is_highway else "AC"}-{charger_number:02d}',
                    defaults={
                        'power_type': power_type,
                        'connector_type': 'CCS2' if is_highway else 'Type 2',
                        'max_power_kw': Decimal('88') if is_highway else Decimal('22'),
                        'status': status_cycle[index % len(status_cycle)],
                        'is_demo': True,
                    },
                )

        ChargingStation.objects.filter(
            slug__in=['demo-accra-central', 'demo-tema-roadside', 'demo-kumasi-hub', 'demo-cape-coast-point'],
            is_demo=True,
        ).update(is_published=False)

        self.stdout.write(self.style.SUCCESS('Loaded 3 illustrative BYD listings and 7 illustrative charging host sites.'))
        self.stdout.write('Demo inventory: 50 x 22 kW Type 2 AC chargers, 3 x 88 kW CCS2 chargers near Suhum and 2 x 88 kW CCS2 chargers near Winneba.')
        self.stdout.write('All prices, vehicle details, coordinates, locations and charger statuses are illustrative only.')
