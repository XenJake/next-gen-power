from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0002_vehicle_is_demo_alter_vehicle_body_style'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicleimage',
            name='image',
            field=models.ImageField(blank=True, upload_to='vehicles/'),
        ),
        migrations.AddField(
            model_name='vehicleimage',
            name='image_url',
            field=models.URLField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name='vehicleimage',
            name='source_url',
            field=models.URLField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name='vehicleimage',
            name='credit',
            field=models.CharField(blank=True, max_length=180),
        ),
        migrations.AddField(
            model_name='vehicleimage',
            name='license_name',
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name='vehicleimage',
            name='license_url',
            field=models.URLField(blank=True, max_length=500),
        ),
    ]
