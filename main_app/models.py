from django.db import models
from django.db.models import Model 
from django.contrib.auth.models import User

# Create your models here.


class EntrepriseModel(Model):
	nom = models.CharField(max_length=255)
	codePostale = models.CharField(max_length=255)
	user = models.ForeignKey(User, on_delete=models.CASCADE)


class JeuDeDonneesModel(Model):
	nom = models.CharField(max_length=255)
	data = models.FileField(upload_to="media/dataset")
	clusters = models.FileField(upload_to="media/clusters", null=True)
	nb_clusters = models.IntegerField(default=0)
	entreprise = models.ForeignKey(EntrepriseModel, on_delete=models.CASCADE, null=True)


class AttributModel(Model):
	utilisateur = models.CharField(max_length=255)
	date_action = models.CharField(max_length=255)
	nom_action = models.CharField(max_length=255)
	montant = models.CharField(max_length=255)
	jeu_de_donnees = models.ForeignKey(JeuDeDonneesModel, on_delete=models.CASCADE)


