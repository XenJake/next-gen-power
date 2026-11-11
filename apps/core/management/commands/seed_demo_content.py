from decimal import Decimal

from django.core.management.base import BaseCommand

from apps.charging.models import Charger, ChargingStation
from apps.vehicles.models import Manufacturer, Vehicle, VehicleImage


VEHICLE_GALLERY = {
    'byd-sealion': [
        ('https://thumb.wikimedia.org/wikipedia/commons/thumb/b/b6/2024_BYD_Sealion_7_3.jpg/1280px-2024_BYD_Sealion_7_3.jpg', 'https://commons.wikimedia.org/wiki/File:2024_BYD_Sealion_7_3.jpg', 'Agratsa', 'CC0', 'https://creativecommons.org/publicdomain/zero/1.0/'),
        ('https://thumb.wikimedia.org/wikipedia/commons/thumb/b/b0/2024_BYD_Sealion_7_Performance_AWD_%28Thailand%29_front_view.png/1280px-2024_BYD_Sealion_7_Performance_AWD_%28Thailand%29_front_view.png', 'https://commons.wikimedia.org/wiki/File:2024_BYD_Sealion_7_Performance_AWD_(Thailand)_front_view.png', 'iMoD Official', 'CC BY 3.0', 'https://creativecommons.org/licenses/by/3.0/'),
        ('https://thumb.wikimedia.org/wikipedia/commons/thumb/e/e6/2024_BYD_Sealion_7_Performance_AWD_%28Thailand%29_rear_view.png/1280px-2024_BYD_Sealion_7_Performance_AWD_%28Thailand%29_rear_view.png', 'https://commons.wikimedia.org/wiki/File:2024_BYD_Sealion_7_Performance_AWD_(Thailand)_rear_view.png', 'iMoD Official', 'CC BY 3.0', 'https://creativecommons.org/licenses/by/3.0/'),
        ('https://thumb.wikimedia.org/wikipedia/commons/thumb/b/b8/2024_BYD_Sealion_7_Premium.jpg/1280px-2024_BYD_Sealion_7_Premium.jpg', 'https://commons.wikimedia.org/wiki/File:2024_BYD_Sealion_7_Premium.jpg', 'Chanokchon', 'CC BY-SA 4.0', 'https://creativecommons.org/licenses/by-sa/4.0/'),
        ('https://thumb.wikimedia.org/wikipedia/commons/thumb/6/65/2025_BYD_Sealion_7_Performance_front.jpg/1280px-2025_BYD_Sealion_7_Performance_front.jpg', 'https://commons.wikimedia.org/wiki/File:2025_BYD_Sealion_7_Performance_front.jpg', 'LuvsMG481', 'CC BY-SA 4.0', 'https://creativecommons.org/licenses/by-sa/4.0/'),
    ],
    'jetour-t2': [
        ('https://thumb.wikimedia.org/wikipedia/commons/thumb/a/ae/Jetour_T2.jpg/1280px-Jetour_T2.jpg', 'https://commons.wikimedia.org/wiki/File:Jetour_T2.jpg', 'Milhouse35', 'CC BY-SA 4.0', 'https://creativecommons.org/licenses/by-sa/4.0/'),
        ('https://thumb.wikimedia.org/wikipedia/commons/thumb/4/42/Jetour_T2_2.0T_Beyond_XWD_Gobi_Beige_01.jpg/1280px-Jetour_T2_2.0T_Beyond_XWD_Gobi_Beige_01.jpg', 'https://commons.wikimedia.org/wiki/File:Jetour_T2_2.0T_Beyond_XWD_Gobi_Beige_01.jpg', 'Ethan Llamas', 'CC BY-SA 4.0', 'https://creativecommons.org/licenses/by-sa/4.0/'),
        ('https://thumb.wikimedia.org/wikipedia/commons/thumb/c/c9/Jetour_T2_2.0T_Beyond_XWD_Gobi_Beige_02.jpg/1280px-Jetour_T2_2.0T_Beyond_XWD_Gobi_Beige_02.jpg', 'https://commons.wikimedia.org/wiki/File:Jetour_T2_2.0T_Beyond_XWD_Gobi_Beige_02.jpg', 'Ethan Llamas', 'CC BY-SA 4.0', 'https://creativecommons.org/licenses/by-sa/4.0/'),
        ('https://thumb.wikimedia.org/wikipedia/commons/thumb/d/d2/Jetour_T2_2.0T_Beyond_XWD_Panda_White_01.jpg/1280px-Jetour_T2_2.0T_Beyond_XWD_Panda_White_01.jpg', 'https://commons.wikimedia.org/wiki/File:Jetour_T2_2.0T_Beyond_XWD_Panda_White_01.jpg', 'Ethan Llamas', 'CC BY-SA 4.0', 'https://creativecommons.org/licenses/by-sa/4.0/'),
        ('https://thumb.wikimedia.org/wikipedia/commons/thumb/0/0f/Jetour_T2_2.0T_Beyond_XWD_Panda_White_02.jpg/1280px-Jetour_T2_2.0T_Beyond_XWD_Panda_White_02.jpg', 'https://commons.wikimedia.org/wiki/File:Jetour_T2_2.0T_Beyond_XWD_Panda_White_02.jpg', 'Ethan Llamas', 'CC BY-SA 4.0', 'https://creativecommons.org/licenses/by-sa/4.0/'),
    ],
    'geely-galaxy-e5': [
        ('https://thumb.wikimedia.org/wikipedia/commons/thumb/3/32/Geely_Galaxy_E5_001.jpg/1280px-Geely_Galaxy_E5_001.jpg', 'https://commons.wikimedia.org/wiki/File:Geely_Galaxy_E5_001.jpg', 'JustAnotherCarDesigner', 'CC0', 'https://creativecommons.org/publicdomain/zero/1.0/'),
        ('https://thumb.wikimedia.org/wikipedia/commons/thumb/a/a1/Geely_Galaxy_E5_002.jpg/1280px-Geely_Galaxy_E5_002.jpg', 'https://commons.wikimedia.org/wiki/File:Geely_Galaxy_E5_002.jpg', 'JustAnotherCarDesigner', 'CC0', 'https://creativecommons.org/publicdomain/zero/1.0/'),
        ('https://thumb.wikimedia.org/wikipedia/commons/thumb/e/ed/Geely_Galaxy_E5_003.jpg/1280px-Geely_Galaxy_E5_003.jpg', 'https://commons.wikimedia.org/wiki/File:Geely_Galaxy_E5_003.jpg', 'JustAnotherCarDesigner', 'CC0', 'https://creativecommons.org/publicdomain/zero/1.0/'),
        ('https://thumb.wikimedia.org/wikipedia/commons/thumb/7/7a/Geely_Galaxy_E5_004.jpg/1280px-Geely_Galaxy_E5_004.jpg', 'https://commons.wikimedia.org/wiki/File:Geely_Galaxy_E5_004.jpg', 'JustAnotherCarDesigner', 'CC0', 'https://creativecommons.org/publicdomain/zero/1.0/'),
        ('https://thumb.wikimedia.org/wikipedia/commons/thumb/1/15/Geely_Galaxy_E5_005.jpg/1280px-Geely_Galaxy_E5_005.jpg', 'https://commons.wikimedia.org/wiki/File:Geely_Galaxy_E5_005.jpg', 'JustAnotherCarDesigner', 'CC0', 'https://creativecommons.org/publicdomain/zero/1.0/'),
    ],
    'xpeng-g7': [
        ('https://thumb.wikimedia.org/wikipedia/commons/thumb/1/18/XPeng_G7_001.jpg/1280px-XPeng_G7_001.jpg', 'https://commons.wikimedia.org/wiki/File:XPeng_G7_001.jpg', 'KitsuneDP', 'CC0', 'https://creativecommons.org/publicdomain/zero/1.0/'),
        ('https://thumb.wikimedia.org/wikipedia/commons/thumb/e/ea/XPeng_G7_002.jpg/1280px-XPeng_G7_002.jpg', 'https://commons.wikimedia.org/wiki/File:XPeng_G7_002.jpg', 'KitsuneDP', 'CC0', 'https://creativecommons.org/publicdomain/zero/1.0/'),
        ('https://thumb.wikimedia.org/wikipedia/commons/thumb/4/44/XPeng_G7_003.jpg/1280px-XPeng_G7_003.jpg', 'https://commons.wikimedia.org/wiki/File:XPeng_G7_003.jpg', 'KitsuneDP', 'CC0', 'https://creativecommons.org/publicdomain/zero/1.0/'),
        ('https://thumb.wikimedia.org/wikipedia/commons/thumb/2/22/XPeng_G7_004.jpg/1280px-XPeng_G7_004.jpg', 'https://commons.wikimedia.org/wiki/File:XPeng_G7_004.jpg', 'KitsuneDP', 'CC0', 'https://creativecommons.org/publicdomain/zero/1.0/'),
        ('https://thumb.wikimedia.org/wikipedia/commons/thumb/1/12/XPeng_G7_005.jpg/1280px-XPeng_G7_005.jpg', 'https://commons.wikimedia.org/wiki/File:XPeng_G7_005.jpg', 'KitsuneDP', 'CC0', 'https://creativecommons.org/publicdomain/zero/1.0/'),
    ],
    'tesla-model-3': [
        ('https://thumb.wikimedia.org/wikipedia/commons/thumb/4/45/2019_Tesla_Model_3_Performance_AWD.jpg/1280px-2019_Tesla_Model_3_Performance_AWD.jpg', 'https://commons.wikimedia.org/wiki/File:2019_Tesla_Model_3_Performance_AWD.jpg', 'Calreyn88', 'CC BY-SA 4.0', 'https://creativecommons.org/licenses/by-sa/4.0/'),
        ('https://thumb.wikimedia.org/wikipedia/commons/thumb/7/77/2024_Tesla_Model_3_%2813103%29.jpg/1280px-2024_Tesla_Model_3_%2813103%29.jpg', 'https://commons.wikimedia.org/wiki/File:2024_Tesla_Model_3_(13103).jpg', 'Calreyn88', 'CC BY-SA 4.0', 'https://creativecommons.org/licenses/by-sa/4.0/'),
        ('https://thumb.wikimedia.org/wikipedia/commons/thumb/9/97/Tesla_Model_3%2C_EMS_2024%2C_Essen_%28P1032260%29.jpg/1280px-Tesla_Model_3%2C_EMS_2024%2C_Essen_%28P1032260%29.jpg', 'https://commons.wikimedia.org/wiki/File:Tesla_Model_3,_EMS_2024,_Essen_(P1032260).jpg', 'Matti Blume', 'CC BY-SA 4.0', 'https://creativecommons.org/licenses/by-sa/4.0/'),
        ('https://thumb.wikimedia.org/wikipedia/commons/thumb/e/ed/Tesla_Model_3_%282023%29_1X7A1678.jpg/1280px-Tesla_Model_3_%282023%29_1X7A1678.jpg', 'https://commons.wikimedia.org/wiki/File:Tesla_Model_3_(2023)_1X7A1678.jpg', 'Alexander-93', 'CC BY-SA 4.0', 'https://creativecommons.org/licenses/by-sa/4.0/'),
        ('https://thumb.wikimedia.org/wikipedia/commons/thumb/e/e6/Tesla_Model_3_%282023%29_Auto_Zuerich_2023_1X7A1313.jpg/1280px-Tesla_Model_3_%282023%29_Auto_Zuerich_2023_1X7A1313.jpg', 'https://commons.wikimedia.org/wiki/File:Tesla_Model_3_(2023)_Auto_Zuerich_2023_1X7A1313.jpg', 'Alexander-93', 'CC BY-SA 4.0', 'https://creativecommons.org/licenses/by-sa/4.0/'),
    ],
    'aito-m9': [
        ('https://thumb.wikimedia.org/wikipedia/commons/thumb/2/20/AITO_M9.jpg/1280px-AITO_M9.jpg', 'https://commons.wikimedia.org/wiki/File:AITO_M9.jpg', 'CNHowey', 'CC0', 'https://creativecommons.org/publicdomain/zero/1.0/'),
        ('https://thumb.wikimedia.org/wikipedia/commons/thumb/8/85/AITO_M9_20231120.jpg/1280px-AITO_M9_20231120.jpg', 'https://commons.wikimedia.org/wiki/File:AITO_M9_20231120.jpg', 'Nissangeniss', 'CC BY-SA 4.0', 'https://creativecommons.org/licenses/by-sa/4.0/'),
        ('https://thumb.wikimedia.org/wikipedia/commons/thumb/4/4c/AITO_M9_20240313_02.jpg/1280px-AITO_M9_20240313_02.jpg', 'https://commons.wikimedia.org/wiki/File:AITO_M9_20240313_02.jpg', '毕明明', 'CC BY-SA 4.0', 'https://creativecommons.org/licenses/by-sa/4.0/'),
        ('https://thumb.wikimedia.org/wikipedia/commons/thumb/9/91/AITO_M9_II_001.jpg/1280px-AITO_M9_II_001.jpg', 'https://commons.wikimedia.org/wiki/File:AITO_M9_II_001.jpg', 'JustAnotherCarDesigner', 'CC0', 'https://creativecommons.org/publicdomain/zero/1.0/'),
        ('https://thumb.wikimedia.org/wikipedia/commons/thumb/5/5f/AITO_M9_II_002.jpg/1280px-AITO_M9_II_002.jpg', 'https://commons.wikimedia.org/wiki/File:AITO_M9_II_002.jpg', 'JustAnotherCarDesigner', 'CC0', 'https://creativecommons.org/publicdomain/zero/1.0/'),
    ],
}


class Command(BaseCommand):
    help = 'Load the vehicle catalogue and Greater Accra demo charging sites.'

    def handle(self, *args, **options):
        vehicles = [
            {
                'manufacturer': 'BYD', 'model_name': 'Sealion', 'slug': 'byd-sealion',
                'price': Decimal('40000'),
            },
            {
                'manufacturer': 'Jetour', 'model_name': 'T2', 'slug': 'jetour-t2',
                'price': Decimal('25000'),
            },
            {
                'manufacturer': 'Geely', 'model_name': 'Galaxy E5', 'slug': 'geely-galaxy-e5',
                'price': Decimal('17000'),
            },
            {
                'manufacturer': 'XPeng', 'model_name': 'G7', 'slug': 'xpeng-g7',
                'price': Decimal('74000'),
            },
            {
                'manufacturer': 'Tesla', 'model_name': 'Model 3', 'slug': 'tesla-model-3',
                'price': Decimal('94000'),
            },
            {
                'manufacturer': 'AITO', 'model_name': 'M9', 'slug': 'aito-m9',
                'price': Decimal('100000'),
            },
        ]
        vehicle_slugs = [values['slug'] for values in vehicles]
        for index, values in enumerate(vehicles):
            manufacturer, _ = Manufacturer.objects.get_or_create(name=values['manufacturer'])
            vehicle, _ = Vehicle.objects.update_or_create(
                slug=values['slug'],
                defaults={
                    **values,
                    'manufacturer': manufacturer,
                    'description': 'Drop-shipped vehicle. Contact us to confirm current availability, specifications and delivery arrangements.',
                    'currency': 'USD',
                    'availability': Vehicle.Availability.ENQUIRE,
                    'is_featured': True,
                    'is_published': True,
                    'is_demo': False,
                },
            )
            for position, (image_url, source_url, credit, license_name, license_url) in enumerate(VEHICLE_GALLERY[vehicle.slug]):
                image_extension = image_url.split('?', maxsplit=1)[0].rsplit('.', maxsplit=1)[-1]
                VehicleImage.objects.update_or_create(
                    vehicle=vehicle,
                    position=position,
                    defaults={
                        'image_url': image_url,
                        'local_path': f'images/vehicles/{vehicle.slug}-{position + 1}.{image_extension}',
                        'source_url': source_url,
                        'alt_text': f'{vehicle.manufacturer.name} {vehicle.model_name} photo {position + 1}',
                        'credit': credit,
                        'license_name': license_name,
                        'license_url': license_url,
                    },
                )
        Vehicle.objects.filter(is_demo=True).exclude(slug__in=vehicle_slugs).update(is_published=False)

        sites = [
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
                'name': 'Demo The Junction Mall', 'slug': 'demo-the-junction-mall',
                'address': 'The Junction Mall, Nungua, Greater Accra', 'city': 'Accra', 'region': 'Greater Accra',
                'site_type': ChargingStation.SiteType.MALL,
            },
            {
                'name': 'Demo Palace Mall Center', 'slug': 'demo-palace-mall-center',
                'address': 'Palace Mall Center, Greater Accra', 'city': 'Accra', 'region': 'Greater Accra',
                'site_type': ChargingStation.SiteType.MALL,
            },
            {
                'name': 'Demo Community 25', 'slug': 'demo-community-25',
                'address': 'Community 25, Tema, Greater Accra', 'city': 'Tema', 'region': 'Greater Accra',
                'site_type': ChargingStation.SiteType.OTHER,
            },
            {
                'name': 'Demo One Airport Square', 'slug': 'demo-one-airport-square',
                'address': 'South Liberation Link, Airport City, Accra', 'city': 'Accra', 'region': 'Greater Accra',
                'site_type': ChargingStation.SiteType.OFFICE,
                'latitude': Decimal('5.6007783'), 'longitude': Decimal('-0.1772592'),
            },
        ]
        site_slugs = [site['slug'] for site in sites]
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
        for site in sites:
            station, _ = ChargingStation.objects.update_or_create(
                slug=site['slug'],
                defaults={
                    'name': site['name'],
                    'address': site['address'],
                    'site_type': site['site_type'],
                    'city': site['city'],
                    'region': site['region'],
                    'latitude': site.get('latitude'),
                    'longitude': site.get('longitude'),
                    'opening_hours': 'Illustrative host-site hours; confirm with the property.',
                    'amenities': 'Demonstration location only. No NEXT GEN POWER charging equipment is deployed here.',
                    'status': ChargingStation.Status.OPERATIONAL,
                    'is_published': True,
                    'is_demo': True,
                },
            )
            for index in range(10):
                charger_number = index + 1
                Charger.objects.update_or_create(
                    station=station,
                    charger_code=f'AC-{charger_number:02d}',
                    defaults={
                        'power_type': Charger.PowerType.AC,
                        'connector_type': 'Type 2',
                        'max_power_kw': Decimal('22'),
                        'status': status_cycle[index % len(status_cycle)],
                        'is_demo': True,
                    },
                )

        ChargingStation.objects.filter(is_demo=True).exclude(slug__in=site_slugs).update(is_published=False)

        self.stdout.write(self.style.SUCCESS('Loaded 6 vehicle listings and 7 Greater Accra demo charging sites.'))
        self.stdout.write('Vehicles are drop-shipped; availability and delivery should be confirmed with the team.')
        self.stdout.write('All charging locations and charger states are demonstrations, not deployment commitments or live availability.')
