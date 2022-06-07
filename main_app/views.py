from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django import forms
from django.core.files import File
from django.http import HttpResponse
import pandas as pd
import numpy as np

import csv
from pathlib import Path
import numpy as np
import os

from main_app import forms as fm
from main_app import models
from clustering.clustering_pdv import culster_data_pdv_kmean


# Create your views here.

class Cellule:
	def __init__(self, col, val_manquante):
		self.col = col
		self.val_manquante = val_manquante


class AccueilView(TemplateView):

	def get(self, request):
		return render(request, "main_app/acceuil.html")

	def post(self):
		pass


class ConnexionView(TemplateView):

	def get(self, request):
		return render(request, "main_app/connexion.html", {"form":fm.ConnexionForm()})

	def post(self, request):
		formuser = fm.ConnexionForm(self.request.POST)
		if formuser.is_valid():
			log = formuser.cleaned_data["login"]
			passw = formuser.cleaned_data["password"]
			user = authenticate(request, username=log, password=passw)
			if user:
				login(request, user)
				entreprise = models.EntrepriseModel.objects.filter(user=user).first()
				data = models.JeuDeDonneesModel.objects.filter(entreprise=entreprise)
				if data.exists():
					data = data.first()
					return redirect(f"/affichedata/{data.id}/", foo=AfficheDataView)
				else:
					return redirect("/upload/", foo=UploadView)
			else:
				return redirect("/inscription/", foo=InscriptionView)
		else:
			return redirect("/connexion/", foo=ConnexionView)


class InscriptionView(TemplateView):

	def get(self, request):
		return render(request, "main_app/inscription.html", {"form":fm.InscriptionForm()})

	def post(self, request):
		inscrit = fm.InscriptionForm(self.request.POST)
		if inscrit.is_valid():
			user = inscrit.save()
			login(request, user)
			return redirect("/upload/", foo=UploadView)
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
			id_data=form.save()
			return redirect(f"/adapte/{id_data}/", foo=AfficheDataView)
		return render(request, 'main_app/upload.html', {"form":form})


class PreprocessView(TemplateView):

	def get(self, request, id):
		jeu_actuelle =  models.JeuDeDonneesModel.objects.get(pk=id)
		path_data = jeu_actuelle.data.name
		data = pd.read_csv(path_data)
		context = {"id": id, "columns" : []}
		a_une_vm = 0
		for col in data.columns:
			val_manquante = data[col].isnull().sum()
			context["columns"].append(Cellule(col,val_manquante))
			a_une_vm += val_manquante
		if a_une_vm>0:
			return render(request, 'main_app/suppresion_vm.html', context)
		else:
			return redirect(f"/verifi_data/{id}/", foo=VerificationDataView)

	def post(self, request, id):
		jeu_actuelle =  models.JeuDeDonneesModel.objects.get(pk=id)
		path_data = jeu_actuelle.data.name
		data = pd.read_csv(path_data)
		for col in data.columns:
			#Selection des données non manquantes
			col_valm = [not val for val in data[col].isnull()]
			data = data[col_valm]
		data["id"] = np.arange(len(data))
		data.set_index("id", inplace=True)
		data.reset_index()
		data.to_csv(path_data)
		return redirect(f"/verifi_data/{id}/", foo=VerificationDataView)


class AfficheDataView(TemplateView):

	def get(self, request, id):
		jeu_actuelle =  models.JeuDeDonneesModel.objects.get(pk=id)
		path_data = jeu_actuelle.data.name
		data = pd.read_csv(path_data)
		context = {"data": data}
		return render(request, "main_app/affichage.html", context)


class AdaptationDataView(TemplateView):

	def get(self, request, id):
		jeu_actuelle =  models.JeuDeDonneesModel.objects.get(pk=id)
		formulaire = fm.AdaptationDataForm()
		path_data = jeu_actuelle.data.name
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
		jeu_actuelle =  models.JeuDeDonneesModel.objects.get(pk=id)
		path_data = jeu_actuelle.data.name
		data = pd.read_csv(path_data)
		
		formulaire.is_valid()
		colonnes = list(formulaire.cleaned_data.keys())
		for col in colonnes :
			data[col] = data[formulaire.cleaned_data[col]]
		data.to_csv(path_data)
		data["id"] = np.arange(len(data))
		data.set_index("id", inplace=True)
		data.reset_index()
		return redirect(f"/supp_vm/{id}/", foo=AfficheDataView)


class VerificationDataView(TemplateView):

	def get(self, request, id):
		jeu_actuelle =  models.JeuDeDonneesModel.objects.get(pk=id)
		path_data = jeu_actuelle.data.name
		data = pd.read_csv(path_data)
		data_conforme = True
		if data["montant"].dtype != np.dtype("float") and data["montant"].dtype!=np.dtype("int") :
			jeu_actuelle.delete()
			os.remove(path_data)
			data_conforme = False
			return render(request, "main_app/data_non_comforme.html",)
		return redirect(f"/segmentation/{id}/", foo=SegmentationView)

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


class SegmentationView(TemplateView):

	def get(self, request, id):
		formulaire = fm.NbClustersForm()
		formulaire.fields["nb_clusters"] = forms.IntegerField()
		context = {"form": formulaire}
		return render(request, "main_app/segmentation.html",context)

	def post(self, request, id):
		form = fm.NbClustersForm(self.request.POST)
		form.is_valid()
		nb_segment = int(form.cleaned_data["nb_clusters"])
		nb_segment = nb_segment if nb_segment>0 else -1*nb_clusters
		jeu_actuelle =  models.JeuDeDonneesModel.objects.get(pk=id)
		path_data = jeu_actuelle.data.name
		cluster = culster_data_pdv_kmean(path_data, nb_segment)
		path_data = f"segment_{id}.csv"
		cluster.to_csv(path_data)
		path = Path(path_data)
		f = path.open(mode="r")
		try:
			os.remove(jeu_actuelle.clusters.name)
		except:
			pass
		jeu_actuelle.clusters = File(f, name=path.name)
		jeu_actuelle.nb_clusters = nb_segment
		jeu_actuelle.save()
		
		return redirect(f"/telechargement/{id}/{nb_segment}/", foo=DownloadSegmentView)


class DownloadSegmentView(TemplateView):

	def get(self, request, id, nb_segment):
		context = {"id_data":id, "liste_cluster":[i for i in range(nb_segment)]}
		return render(request, "main_app/download_clusters.html", context)


class EnvoiSegmentView(TemplateView):

	def get(self, request, id, segment):
		jeu_actuelle =  models.JeuDeDonneesModel.objects.get(pk=id)
		path_data = jeu_actuelle.clusters.name
		clusters = pd.read_csv(path_data)
		clusters = clusters[clusters["classes"]==segment]
		clusters = clusters["pdv"].tolist()
		
		#Create the HttpResponse object with the appropriate CSV header.
		response = HttpResponse(
			content_type='text/csv',
			headers={'Content-Disposition': f'attachment; filename="segment_{segment}.csv"'},
			)
		writer = csv.writer(response)
		writer.writerow(['points de vente'])
		for pdv in clusters:
			writer.writerow([pdv])
		return response



