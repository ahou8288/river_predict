# Generated by Django 2.0.1 on 2018-01-11 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rivers', '0002_auto_20180109_2252'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='slug',
            field=models.SlugField(default='def'),
            preserve_default=False,
        ),
    ]
