# Generated by Django 5.0.1 on 2024-03-07 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emr', '0036_billing_payment_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='is_scheduled',
            field=models.BooleanField(default=False),
        ),
    ]
