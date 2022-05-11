from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
import pandas as pd

from main_app import forms
from main_app import models

# Create your views here.


class Cellule:
	def __init__(self, col, val_manquante):
		self.col = col
		self.val_manquante = val_manquante


class UploadView(TemplateView):

	def get(self, request):
		form = forms.UploadDataForm(request.POST, request.FILES)
		return render(request, 'main_app/upload.html', {"form":form})

	def post(self, request):
		form = forms.UploadDataForm(request.POST, request.FILES)
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
		data.to_csv(path_data)
		return redirect(f"/preprocess1/{id}", foo=PreprocessView)
		#return redirect("preprocess1")


class AfficheData(TemplateView):

	def get(self, request, id):
		jeu_actuelle =  models.JeuDeDonnees.objects.get(pk=id)
		path_data = jeu_actuelle.file.name
		data = pd.read_csv(path_data)
		context = {"data": data}
		return render(request, "main_app/affichage.html", context)


