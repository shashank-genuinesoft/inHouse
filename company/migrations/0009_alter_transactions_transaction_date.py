# Generated by Django 4.0.6 on 2022-08-08 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0008_alter_transactions_transaction_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='transaction_date',
            field=models.DateField(),
        ),
    ]