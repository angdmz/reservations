# Generated by Django 2.2.6 on 2019-11-13 12:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zones', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='country',
            options={'verbose_name': 'Destino', 'verbose_name_plural': 'Destinos'},
        ),
        migrations.AlterModelTable(
            name='country',
            table='destinations',
        ),
    ]
