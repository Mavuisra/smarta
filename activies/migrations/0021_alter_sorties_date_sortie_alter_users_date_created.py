# Generated by Django 4.1.3 on 2022-12-19 17:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activies', '0020_alter_sorties_date_sortie_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sorties',
            name='date_sortie',
            field=models.DateTimeField(default='2022-12-19 18:55:54.529924'),
        ),
        migrations.AlterField(
            model_name='users',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 19, 18, 55, 54, 529924)),
        ),
    ]
