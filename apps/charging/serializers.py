from rest_framework import serializers

from .models import Charger, ChargingStation


class ChargerStatusSerializer(serializers.ModelSerializer):
    status_label = serializers.CharField(source='get_status_display', read_only=True)
    station_name = serializers.CharField(source='station.name', read_only=True)

    class Meta:
        model = Charger
        fields = ['public_id', 'charger_code', 'power_type', 'connector_type', 'max_power_kw', 'status', 'status_label', 'station_name', 'last_heartbeat_at']


class StationSerializer(serializers.ModelSerializer):
    available_chargers = serializers.SerializerMethodField()
    charger_count = serializers.IntegerField(source='chargers.count', read_only=True)

    class Meta:
        model = ChargingStation
        fields = ['name', 'slug', 'site_type', 'address', 'city', 'region', 'latitude', 'longitude', 'status', 'available_chargers', 'charger_count', 'solar_capacity_kw', 'battery_storage_kwh', 'is_demo']

    def get_available_chargers(self, station):
        return station.chargers.filter(status=Charger.Status.AVAILABLE).count()
