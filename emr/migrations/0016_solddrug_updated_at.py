# Generated by Django 5.0.1 on 2024-02-21 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emr', '0015_solddrug_order_id_alter_solddrug_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='solddrug',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]