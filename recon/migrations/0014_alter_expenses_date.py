# Generated by Django 4.0.4 on 2022-06-30 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recon', '0013_photos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenses',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
