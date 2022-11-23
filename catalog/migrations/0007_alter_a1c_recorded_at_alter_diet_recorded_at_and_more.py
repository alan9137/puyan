# Generated by Django 4.1.2 on 2022-11-16 06:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_alter_a1c_recorded_at_alter_diet_recorded_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='a1c',
            name='recorded_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='diet',
            name='recorded_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='drug',
            name='recorded_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='pressure',
            name='recorded_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='sugar',
            name='recorded_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='weight',
            name='recorded_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
