# Generated by Django 5.0 on 2024-03-16 19:45

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
            model_name='businesshour',
            name='business',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='business_hours', to='agent.business', verbose_name='Negocio'),
        ),
        migrations.AddField(
            model_name='field',
            name='business',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fields', to='agent.business', verbose_name='Negocio'),
        ),
        migrations.AddField(
            model_name='field',
            name='sport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.sport'),
        ),
        migrations.AddField(
            model_name='fieldpricerange',
            name='field',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='price_ranges', to='agent.field', verbose_name='Cancha'),
        ),
        migrations.AddField(
            model_name='mediaimage',
            name='field',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='agent.field', verbose_name='Cancha'),
        ),
        migrations.AddField(
            model_name='services',
            name='business',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='agent.business', verbose_name='Negocio'),
        ),
        migrations.AlterUniqueTogether(
            name='businesshour',
            unique_together={('business', 'day')},
        ),
    ]
