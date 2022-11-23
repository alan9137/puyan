# Generated by Django 4.1.2 on 2022-11-16 06:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_alter_a1c_recorded_at_alter_diet_recorded_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='a1c',
            name='recorded_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 16, 6, 19, 53, 186326, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='diet',
            name='recorded_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 16, 6, 19, 53, 188330, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='drug',
            name='recorded_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 16, 6, 19, 53, 189325, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='pressure',
            name='recorded_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 16, 6, 19, 53, 185325, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='sugar',
            name='recorded_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 16, 6, 19, 53, 186326, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='weight',
            name='recorded_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 16, 6, 19, 53, 186326, tzinfo=datetime.timezone.utc)),
        ),
    ]
