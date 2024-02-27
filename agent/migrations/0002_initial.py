# Generated by Django 5.0 on 2024-02-26 03:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('agent', '0001_initial'),
        ('dashboard', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Usuario admin'),
        ),
        migrations.AddField(
            model_name='field',
            name='business',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agent.business', verbose_name='Negocio'),
        ),
        migrations.AddField(
            model_name='field',
            name='sport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.sport', verbose_name='Deporte'),
        ),
        migrations.AddField(
            model_name='mediaimage',
            name='field',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='agent.field', verbose_name='Cancha'),
        ),
    ]
