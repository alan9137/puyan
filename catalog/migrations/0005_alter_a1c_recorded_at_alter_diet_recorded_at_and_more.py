# Generated by Django 4.1.2 on 2022-11-16 06:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_alter_a1c_recorded_at_alter_diet_recorded_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='a1c',
            name='recorded_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 16, 14, 7, 13, 471656)),
        ),
        migrations.AlterField(
            model_name='diet',
            name='recorded_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 16, 14, 7, 13, 472656)),
        ),
        migrations.AlterField(
            model_name='drug',
            name='recorded_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 16, 14, 7, 13, 473657)),
        ),
        migrations.AlterField(
            model_name='pressure',
            name='recorded_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 16, 14, 7, 13, 469665)),
        ),
        migrations.AlterField(
            model_name='sugar',
            name='recorded_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 16, 14, 7, 13, 470662)),
        ),
        migrations.AlterField(
            model_name='weight',
            name='recorded_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 16, 14, 7, 13, 470662)),
        ),
    ]
