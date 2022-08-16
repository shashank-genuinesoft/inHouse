# Generated by Django 4.0.6 on 2022-08-05 12:31

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0005_transactions_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupmaster',
            name='group_under',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='company.groupmaster'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='companies',
            name='registration_date',
            field=models.DateField(blank=True, default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='created_at',
            field=models.DateField(blank=True, default=datetime.date.today),
        ),
    ]