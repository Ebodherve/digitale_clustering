from django import forms
from main_app import models


class UploadDataForm(forms.Form):

	title = forms.CharField(max_length=255)
	file = forms.FileField()

	def save(self):

		fich = models.JeuDeDonnees()
		fich.title = self.cleaned_data["title"]
		fich.file = self.cleaned_data["file"]
		fich.save()


