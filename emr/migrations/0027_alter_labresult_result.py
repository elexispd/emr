# Generated by Django 5.0.1 on 2024-02-27 13:57

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emr', '0026_patient_card_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='labresult',
            name='result',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
