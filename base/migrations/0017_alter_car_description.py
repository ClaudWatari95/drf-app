# Generated by Django 4.1.5 on 2023-01-22 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_remove_car_count_car_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='description',
            field=models.TextField(default='', null=True),
        ),
    ]
