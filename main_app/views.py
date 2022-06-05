from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django import forms
from django.http import HttpResponse

import pandas as pd
import numpy as np
import csv

from main_app import forms as fm
from main_app import models


# Create your views here.

class Cellule:
	def __init__(self, col, val_manquante):
		self.col = col
		self.val_manquante = val_manquante


class AccueilView(TemplateView):

	def get(self):
		pass

	def post(self):
		pass


class ConnexionView(TemplateView):

	def get(self, request):
		return render(request, "main_app/connexion.html", {"form":forms.ConnexionForm()})

	def post(self, request):
		formuser = fm.ConnexionForm(self.request.POST)
		if formuser.is_valid():
			log = formuser.cleaned_data["login"]
			passw = formuser.cleaned_data["password"]
			user = authenticate(request, username=log, password=passw)
			if user:
				login(request, user)
				#return redirect("connexion", foo=ConnexionView)
				return redirect("")
			else:
				ctx = {}
				#return redirect("connexion", foo=ConnexionView)
				return render(request, "", ctx)
		else:
			ctx = {}
			return redirect("connexion", foo=ConnexionView)
			#return render(request, "", ctx)


class InscriptionView(TemplateView):

	def get(self, request):
		return render(request, "main_app/inscription.html", {"form":forms.InscriptionForm()})

	def post(self, request):
		inscrit = fm.InscriptionForm(self.request.POST)
		if inscrit.is_valid():
			user = inscrit.save()
			login(request, user)
			return redirect("")
		else:
			ctx = {}
			return render(request, "main_app/inscription.html", ctx)


class UploadView(TemplateView):

	def get(self, request):
		form = fm.UploadDataForm(request.POST, request.FILES)
		return render(request, 'main_app/upload.html', {"form":form})

	def post(self, request):
		form = fm.UploadDataForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return redirect("envoi")
		return render("envoi")


class PreprocessView(TemplateView):

	def get(self, request, id):
		jeu_actuelle =  models.JeuDeDonnees.objects.get(pk=id)
		path_data = jeu_actuelle.file.name
		data = pd.read_csv(path_data)
		context = {"id": id, "columns" : []}
		for col in data.columns:
			val_manquante = data[col].isnull().sum()
			context["columns"].append(Cellule(col,val_manquante))
		return render(request, 'main_app/preprocess1.html', context)

	def post(self, request, id):
		jeu_actuelle =  models.JeuDeDonnees.objects.get(pk=id)
		path_data = jeu_actuelle.file.name
		data = pd.read_csv(path_data)
		new_col = [col for col in data.columns if data[col].isnull().sum()==0]
		data = data[new_col]
		data["id"] = np.arange(len(data))
		data.set_index("id", inplace=True)
		data.reset_index()
		data.to_csv(path_data)
		return redirect(f"/preprocess1/{id}", foo=PreprocessView)


class AfficheDataView(TemplateView):

	def get(self, request, id):
		jeu_actuelle =  models.JeuDeDonnees.objects.get(pk=id)
		path_data = jeu_actuelle.file.name
		data = pd.read_csv(path_data)
		context = {"data": data}
		return render(request, "main_app/affichage.html", context)


class AdaptationDataView(TemplateView):

	def get(self, request, id):
		jeu_actuelle =  models.JeuDeDonnees.objects.get(pk=id)
		formulaire = fm.AdaptationDataForm()
		path_data = jeu_actuelle.file.name
		data = pd.read_csv(path_data)
		colonnes = data.columns
		colonnes = [(c, c) for c in colonnes]
		formulaire.fields["date_action"] = forms.ChoiceField(choices=colonnes)
		formulaire.fields["points_de_vente"] = forms.ChoiceField(choices=colonnes)
		formulaire.fields["nom_action"] = forms.ChoiceField(choices=colonnes)
		formulaire.fields["montant"] = forms.ChoiceField(choices=colonnes)
		
		context = {"form":formulaire}
		return render(request, "main_app/adapte.html",context)

	def post(self, request, id):
		formulaire = fm.AdaptationDataForm(request.POST)
		jeu_actuelle =  models.JeuDeDonnees.objects.get(pk=id)
		path_data = jeu_actuelle.file.name
		data = pd.read_csv(path_data)
		
		formulaire.is_valid()
		colonnes = list(formulaire.cleaned_data.keys())
		for col in colonnes :
			data[col] = data[formulaire.cleaned_data[col]]
		data = data[colonnes]
		data["id"] = np.arange(len(data))
		data.set_index("id", inplace=True)
		data.reset_index()
		data.to_csv(path_data)
		return redirect(f"/affichedata/{id}/", foo=AfficheDataView)


class TelechargerView(TemplateView):

	def get(self, request):
		#Create the HttpResponse object with the appropriate CSV header.
		response = HttpResponse(
			content_type='text/csv',
			headers={'Content-Disposition': 'attachment; filename="somefilename.csv"'},
			)
		writer = csv.writer(response)
		writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
		writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])

		return response
		
	def post(self, request):
		pass


