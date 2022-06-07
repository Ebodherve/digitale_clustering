# Generated by Django 3.2.8 on 2022-06-05 13:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EntrepriseModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
                ('codePostale', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='JeuDeDonneesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
                ('data', models.FileField(upload_to='media/dataset')),
                ('clusters', models.FileField(upload_to='media/dataset')),
                ('entreprise', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.entreprisemodel')),
            ],
        ),
        migrations.CreateModel(
            name='AttributModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('utilisateur', models.CharField(max_length=255)),
                ('date_action', models.CharField(max_length=255)),
                ('nom_action', models.CharField(max_length=255)),
                ('montant', models.CharField(max_length=255)),
                ('jeu_de_donnees', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.jeudedonneesmodel')),
            ],
        ),
    ]