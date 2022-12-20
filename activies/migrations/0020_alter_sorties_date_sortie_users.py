# Generated by Django 4.1.3 on 2022-12-19 17:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activies', '0019_alter_sorties_date_sortie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sorties',
            name='date_sortie',
            field=models.DateTimeField(default='2022-12-19 18:46:15.489918'),
        ),
        migrations.CreateModel(
            name='users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('post_nom', models.CharField(max_length=20)),
                ('ville', models.CharField(max_length=20)),
                ('matricule', models.CharField(max_length=20)),
                ('telephone', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=20)),
                ('image_pic', models.ImageField(blank=True, null=True, upload_to='')),
                ('date_created', models.DateTimeField(default='2022-12-19 18:46:15.490920')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
