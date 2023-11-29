# Generated by Django 4.2.7 on 2023-11-28 06:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_remove_card_price_remove_cpu_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='card',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='cpu',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='cpu',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='harddrive',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='harddrive',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='laptop',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='laptop',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='manhinh',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='manhinh',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='ram',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='ram',
            name='discount',
        ),
        migrations.AlterField(
            model_name='discount',
            name='date_end',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 11, 30, 13, 41, 50, 720851), null=True),
        ),
        migrations.AlterField(
            model_name='discount',
            name='date_start',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 11, 28, 13, 41, 50, 720851), null=True),
        ),
    ]