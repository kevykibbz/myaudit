# Generated by Django 3.2.9 on 2022-11-22 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0024_remove_costmodel_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='costmodel',
            name='rating',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
