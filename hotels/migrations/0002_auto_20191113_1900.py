# Generated by Django 2.2.6 on 2019-11-13 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='address',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
