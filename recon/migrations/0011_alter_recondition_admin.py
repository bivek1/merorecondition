# Generated by Django 4.0.4 on 2022-06-25 16:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recon', '0010_order_date_order_seen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recondition',
            name='admin',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='rec_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
