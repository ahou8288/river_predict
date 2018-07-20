# Generated by Django 2.0.1 on 2018-01-24 02:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rivers', '0011_points_sectionpoints'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sectionpoints',
            name='point',
        ),
        migrations.RemoveField(
            model_name='sectionpoints',
            name='section',
        ),
        migrations.AddField(
            model_name='points',
            name='section',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='rivers.Section'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Sectionpoints',
        ),
    ]