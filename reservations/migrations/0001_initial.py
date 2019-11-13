# Generated by Django 2.2.6 on 2019-11-08 19:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('zones', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('external_id', models.CharField(max_length=36)),
                ('destination', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='zones.Country')),
            ],
            options={
                'verbose_name': 'Reservacion',
                'verbose_name_plural': 'Reservaciones',
                'db_table': 'reservations',
            },
        ),
    ]