# Generated by Django 3.2.9 on 2022-10-28 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0005_chatmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmodel',
            name='receiver',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
