# Generated by Django 4.0.4 on 2022-06-24 02:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recon', '0007_category_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='seen',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('number', models.BigIntegerField()),
                ('address', models.CharField(max_length=200)),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicle_order', to='recon.vehicle')),
            ],
        ),
    ]
