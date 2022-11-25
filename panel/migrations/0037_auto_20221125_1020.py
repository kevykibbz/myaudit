# Generated by Django 3.2.9 on 2022-11-25 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0036_readingmodel_datapoint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='costmodel',
            name='consumption',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='readingmodel',
            name='consumption',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
