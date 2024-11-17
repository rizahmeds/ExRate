# Generated by Django 5.1.3 on 2024-11-17 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='currency',
            options={'verbose_name': 'Currency', 'verbose_name_plural': 'Currencies'},
        ),
        migrations.AlterModelOptions(
            name='currencyexchangerate',
            options={'verbose_name': 'Currency Exchange Rate', 'verbose_name_plural': 'Currency Exchange Rates'},
        ),
        migrations.AlterField(
            model_name='currencyexchangerate',
            name='rate_value',
            field=models.DecimalField(db_index=True, decimal_places=6, default=1, max_digits=18),
        ),
    ]
