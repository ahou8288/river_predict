# Generated by Django 2.0.1 on 2018-01-11 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rivers', '0006_auto_20180111_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gauge',
            name='download_id',
            field=models.CharField(max_length=10),
        ),
    ]
