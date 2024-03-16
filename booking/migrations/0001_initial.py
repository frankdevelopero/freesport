# Generated by Django 5.0 on 2024-03-16 19:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('agent', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_fullname', models.CharField(blank=True, max_length=256, null=True, verbose_name='Nombre de la persona')),
                ('user_phone', models.CharField(blank=True, max_length=24, null=True, verbose_name='Número de celular')),
                ('voucher', models.ImageField(blank=True, null=True, upload_to='payments', verbose_name='Comprobante')),
                ('phone', models.TextField(blank=True, max_length=18, null=True)),
                ('start_time', models.DateTimeField(verbose_name='Hora de inicio')),
                ('end_time', models.DateTimeField(verbose_name='Hora de fin')),
                ('status', models.IntegerField(choices=[(1, 'Pendiente'), (2, 'Confirmada'), (3, 'Cancelada'), (4, 'Finalizada')], default=1, verbose_name='Estado')),
                ('price', models.DecimalField(decimal_places=2, editable=False, max_digits=10, verbose_name='Precio')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agent.business', verbose_name='Negocio')),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agent.field', verbose_name='Cancha')),
            ],
            options={
                'verbose_name': 'Reserva',
                'verbose_name_plural': 'Reservas',
            },
        ),
    ]
