# Generated by Django 4.1.3 on 2023-01-11 20:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activies', '0045_alter_sorties_date_sortie_alter_users_date_created_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commande',
            name='prix_total',
        ),
        migrations.AlterField(
            model_name='commande',
            name='date_sortie',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 11, 21, 22, 31, 888872)),
        ),
        migrations.AlterField(
            model_name='sorties',
            name='date_sortie',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 11, 21, 22, 31, 893871)),
        ),
        migrations.AlterField(
            model_name='users',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 11, 21, 22, 31, 893871)),
        ),
    ]