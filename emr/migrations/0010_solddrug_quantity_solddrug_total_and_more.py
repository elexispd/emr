# Generated by Django 5.0.1 on 2024-02-21 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emr', '0009_solddrug'),
    ]

    operations = [
        migrations.AddField(
            model_name='solddrug',
            name='quantity',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='solddrug',
            name='total',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='solddrug',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
