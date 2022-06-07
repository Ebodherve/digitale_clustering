from django import forms
from main_app import models
from django.contrib.auth import get_user_model

User = get_user_model()


class UploadDataForm(forms.Form):

	nom = forms.CharField()
	data = forms.FileField()

	def save(self):

		fich = models.JeuDeDonneesModel()
		fich.nom = self.cleaned_data["nom"]
		fich.data = self.cleaned_data["data"]
		fich.save()
		return fich.id


class ConnexionForm(forms.Form):

	login = forms.CharField()
	password = forms.CharField()


class InscriptionForm(forms.Form):

	firstname = forms.CharField()
	name = forms.CharField()
	email = forms.EmailField()
	password = forms.CharField()
	login = forms.CharField()

	def save(self):
		log = self.cleaned_data["login"]
		name = self.cleaned_data["name"]
		email = self.cleaned_data["email"]
		firstname = self.cleaned_data["firstname"]
		password = self.cleaned_data["password"]
		userinscrit = User.objects.create_user(log, email, password,first_name=firstname, last_name=name)
		return userinscrit


class AdaptationDataForm(forms.Form):

	date_action = forms.CharField()
	points_de_vente = forms.CharField()
	nom_action = forms.CharField()
	montant = forms.CharField()


class NbClustersForm(forms.Form):

	nb_clusters = forms.CharField()


class FiltreAttributForm(forms.Form):

	attribut = forms.CharField()




