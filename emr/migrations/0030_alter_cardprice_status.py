# Generated by Django 5.0.1 on 2024-03-01 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emr', '0029_cardprice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardprice',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
