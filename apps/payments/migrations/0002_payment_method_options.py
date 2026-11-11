from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='method',
            field=models.CharField(
                blank=True,
                choices=[
                    ('mtn_momo', 'MTN Mobile Money'),
                    ('telecel_cash', 'Telecel Cash'),
                    ('at_money', 'AT Money'),
                    ('visa', 'Visa'),
                    ('mastercard', 'Mastercard'),
                    ('mobile_money', 'Mobile money'),
                    ('card', 'Card'),
                ],
                default='',
                max_length=20,
            ),
        ),
    ]
