# Generated by Django 3.0.2 on 2020-05-17 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20200517_1315'),
    ]

    operations = [
        migrations.CreateModel(
            name='BalanceSheet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idd', models.BigIntegerField()),
            ],
            options={
                'verbose_name': 'BalanceSheet',
                'verbose_name_plural': 'BalanceSheet',
            },
        ),
    ]
