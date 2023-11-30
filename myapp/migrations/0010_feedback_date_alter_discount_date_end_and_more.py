# Generated by Django 4.2.7 on 2023-11-30 08:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_remove_feedback_subject_alter_discount_date_end_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='discount',
            name='date_end',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 12, 2, 15, 5, 57, 153503), null=True),
        ),
        migrations.AlterField(
            model_name='discount',
            name='date_start',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 11, 30, 15, 5, 57, 153503), null=True),
        ),
    ]
