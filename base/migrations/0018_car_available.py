# Generated by Django 4.1.5 on 2023-01-22 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_alter_car_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='available',
            field=models.BooleanField(default=True),
        ),
    ]
