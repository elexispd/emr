# Generated by Django 5.0.1 on 2024-03-01 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emr', '0028_card_alter_billing_service_type_billing_card'),
    ]

    operations = [
        migrations.CreateModel(
            name='CardPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_type', models.CharField(choices=[('new', 'New Card'), ('renew', 'Card Renewal')], max_length=20)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.IntegerField(default=1)),
            ],
        ),
    ]
