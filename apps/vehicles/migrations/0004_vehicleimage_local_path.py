from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0003_vehicleimage_external_image_and_attribution'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicleimage',
            name='local_path',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
