# Generated by Django 4.0.4 on 2022-06-25 17:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recon', '0011_alter_recondition_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recondition',
            name='admin',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]