# Generated by Django 4.1.3 on 2022-11-14 23:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='clients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_clients', models.CharField(max_length=50)),
                ('sexe', models.CharField(default='homme', max_length=10)),
                ('telephone', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='fourcasterie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(default='SF', max_length=255)),
                ('date_create', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='fournisseurs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_fournisseurs', models.CharField(max_length=50)),
                ('sexe', models.CharField(default='homme', max_length=10)),
                ('telephone', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='fourrafine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(default='RF', max_length=255)),
                ('date_create', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='produits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomProdui', models.CharField(max_length=20)),
                ('date_creation', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('montant', models.FloatField()),
                ('produits', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activies.produits')),
            ],
        ),
        migrations.CreateModel(
            name='sorties',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prix_vente', models.DecimalField(decimal_places=2, max_digits=8)),
                ('quantite', models.FloatField()),
                ('teneur', models.FloatField()),
                ('tvaPourcentage', models.FloatField()),
                ('date_sortie', models.DateTimeField(auto_now=True)),
                ('clients', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activies.clients')),
                ('produits', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activies.produits')),
            ],
        ),
        migrations.CreateModel(
            name='smelting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantite_entrer', models.FloatField(blank=True, default=0.0, null=True)),
                ('quantite_out', models.FloatField(blank=True, default=0.0, null=True)),
                ('teneur_entrer', models.FloatField()),
                ('date_entrer', models.DateTimeField(auto_now=True)),
                ('entrants', models.FloatField(blank=True, default=0.0, null=True)),
                ('fourcasterie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activies.fourcasterie')),
                ('produits', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activies.produits')),
            ],
        ),
        migrations.CreateModel(
            name='refinering',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantite_sortie', models.FloatField(blank=True, default=0.0, null=True)),
                ('teneur_sortie', models.FloatField()),
                ('date_sortie', models.DateTimeField(auto_now=True)),
                ('entrants', models.FloatField(blank=True, default=0.0, null=True)),
                ('fourrafine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activies.fourrafine')),
                ('produits', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activies.produits')),
            ],
        ),
        migrations.CreateModel(
            name='entrees',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prix_achat', models.FloatField()),
                ('quantite', models.FloatField()),
                ('teneur', models.FloatField()),
                ('numero_tag', models.CharField(max_length=20)),
                ('tvaPourcentage', models.FloatField(max_length=20)),
                ('date_sortie', models.DateTimeField(auto_now=True)),
                ('fournisseurs', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activies.fournisseurs')),
                ('produits', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activies.produits')),
            ],
        ),
    ]