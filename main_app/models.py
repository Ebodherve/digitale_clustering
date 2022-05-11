from django.db import models
from django.db.models import Model 
from django.contrib.auth.models import User

# Create your models here.


class Entreprise(Model):
	nom = models.CharField(max_length=255)
	user = models.ForeignKey(User, on_delete=models.CASCADE)


class JeuDeDonnees(Model):
	nom = models.CharField(max_length=255)
	file = models.FileField(upload_to="media/dataset")
	taille = models.IntegerField(null=True)
	entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, null=True)


class Attribut(Model):
	nom = models.CharField(max_length=255)
	type_attribut = models.CharField(max_length=255)
	jeu_de_donnees = models.ForeignKey(JeuDeDonnees, on_delete=models.CASCADE)


class SegmentAttribut(Model):
	nom = models.CharField(max_length=255)
	nom_op = models.CharField(max_length=255)
	attribut = models.ForeignKey(Attribut, on_delete=models.CASCADE)
	jeu_de_donnees = models.ForeignKey(JeuDeDonnees, on_delete=models.CASCADE)


