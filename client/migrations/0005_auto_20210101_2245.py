# Generated by Django 3.1.4 on 2021-01-01 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0004_auto_20210101_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
    ]
