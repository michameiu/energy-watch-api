# Generated by Django 3.0.8 on 2020-12-26 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_auto_20201014_1559'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='phone',
            field=models.CharField(default='0727289323', max_length=50),
            preserve_default=False,
        ),
    ]
