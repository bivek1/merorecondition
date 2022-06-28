# Generated by Django 4.0.4 on 2022-06-24 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recon', '0009_order_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='order',
            name='seen',
            field=models.BooleanField(default=False),
        ),
    ]
