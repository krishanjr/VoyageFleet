# Generated by Django 4.2.9 on 2024-08-18 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicleManagement', '0003_alter_vehicle_driver_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='end_location',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='booking',
            name='start_location',
            field=models.TextField(),
        ),
    ]
