# Generated by Django 3.0.2 on 2020-05-22 08:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_auto_20200522_1356'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transactions',
            name='cash_in_hand',
        ),
    ]