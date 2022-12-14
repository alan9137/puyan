# Generated by Django 4.1.2 on 2022-11-17 09:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0010_alter_diet_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diet',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diet', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='medical',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='medical', to=settings.AUTH_USER_MODEL),
        ),
    ]
