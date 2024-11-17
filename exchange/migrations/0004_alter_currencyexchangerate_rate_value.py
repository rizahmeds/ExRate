# Generated by Django 5.1.3 on 2024-11-17 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0003_alter_currencyexchangerate_rate_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currencyexchangerate',
            name='rate_value',
            field=models.DecimalField(blank=True, db_index=True, decimal_places=6, max_digits=18, null=True),
        ),
    ]