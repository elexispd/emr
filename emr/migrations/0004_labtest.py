# Generated by Django 5.0.1 on 2024-02-20 12:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emr', '0003_appointment_labprice_alter_appointment_doctor'),
    ]

    operations = [
        migrations.CreateModel(
            name='LabTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emr.appointment')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emr.labprice')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emr.patient')),
            ],
        ),
    ]
