# Generated by Django 3.2.9 on 2022-10-28 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0009_ordermodel_messages'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmodel',
            name='bid_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
