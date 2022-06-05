#Ce module contient des classes et fontions permettant de mettre les données sous une forme adapté à la segmentation
#
#---------------------------------------------------------------------------#

import pandas as pd
import numpy as np
from copy import deepcopy


def extraire_jour(date):
    date = date.split(" ")[0]
    return date

def est_dans_plage(plage, h):
    return plage[0] <=h and h <=plage[1]

def extraire_heure(date):
    date = date.split(" ")[1]
    date = date.split(":")
    return date[2]

def extraire_heure(date):
    date = date.split(" ")[1]
    return date

def creer_plage(ph = ["00:00:00.0", "05:00:00.0", "10:00:00.0", "15:00:00.0", "20:00:00.0", "24:00:00.0"]):
    ph1 = []
    heure_actuelle = ph[0]
    for e in ph[1:]:
        ph1.append((heure_actuelle, e))
        heure_actuelle = e
    return ph1

def trouve_plage(heure, liste_plage):
    for p in liste_plage:
        if heure >= p[0] and heure <= p[1]:
            return p
    return liste_plage[-1]

#Heures limites des plages otenus
heure_limites=["00:00.0", "10:00.0", "20:00.0", "30:00.0", "40:00.0", "50:00.0", "59:00.0"]


class TransformDataPdv:

	def __init__(self, data, heure_limites=heure_limites, col_pdv="pdv"):
		# Dataframe des points de vente
		self.data = data
		# Nouveau dataframe devant etre produit apres transformation
		self.__new_data = None
		# Representation des données des sur les points de vente dans un dictionnaires
		self.pdv_vecteur_dict = None
		#plages horaires
		self.plages_horaires = creer_plage(heure_limites)
		#Colonne correspondant aux points de ventes
		self.col_pdv = col_pdv

	#Fonction d'extraction de la liste des vecteurs points de ventes
	def liste_vecteurs_pdv(self, jour=extraire_jour, heure=extraire_heure):
		lph = self.plages_horaires
		data = self.data
		#creation de la liste des jours
		liste_jour = set()
		for i in range(len(data)):
			e = data["date_action"].loc[i]
			liste_jour = liste_jour.union([jour(e)])

		#tri de cette liste de jours dans l'ordre croissant
		liste_jour = sorted(list(liste_jour))

		#initialisation du type de structure d'une plage horaire
		liste_action = data["nom_action"].unique()
		plage_h_contenus = {val:{'nombre':0, 'montant_total':0} for val in liste_action}

		#Initialisation du type de structure d'une journée
		plage_j_contenus = {plage_h:deepcopy(plage_h_contenus) for plage_h in lph}

		# initialisation du type de structure des points de ventes
		info_pdv = data["utilisateur"].unique()
		liste_pdv = {}
		for pdv in info_pdv:
			liste_pdv[pdv] = {j:deepcopy(plage_j_contenus) for j in liste_jour}

		# remplissage des structures formés
		for i in range(len(data)):
			ligne = data.loc[i]
			pdv = liste_pdv[ligne["utilisateur"]]
			jour_ = pdv[jour(ligne["date_action"])]
			plage = trouve_plage(heure(ligne["date_action"]), lph)
			plage = jour_[plage]
			action = plage[ligne["nom_action"]]
			action["nombre"] += 1
			action["montant_total"] += ligne["montant"]

		self.pdv_vecteur_dict = liste_pdv

	# Fonction permettant de stocker un dictionnaire des points vente dans un data frame
	def construction_df(self, nombre="nombre", montant="montant_total", entete=False):
		pdv = self.col_pdv
		dict_pdv = self.pdv_vecteur_dict
		struct_pdv = {}
		for pdvname, pdv in dict_pdv.items():
			vecteur_pdv = []
			for jour in pdv.values():
				for plage in jour.values():
					for action in plage.values():
						vecteur_pdv.append(int(action[nombre]))
						vecteur_pdv.append(action[montant])
			struct_pdv[pdvname] = vecteur_pdv
		if not entete:
			indexes = []
			pdv1 = list(dict_pdv.values())[0]
			for nom_j, jour in pdv1.items():
				for nom_p, plage in jour.items():
					for nom_a, action in  plage.items():
						nbr = "jour "+str(nom_j)+" plage : "+str(nom_p)+" action "+str(nom_a)+" Nombre"
						mont = "jour "+str(nom_j)+" plage : "+str(nom_p)+" action"+str(nom_a)+" Montant"
						indexes.append(nbr)
						indexes.append(mont)
		df = pd.DataFrame(struct_pdv, index=indexes).transpose()
		df = df.reset_index()
		df[self.col_pdv] = df["index"]
		del df["index"]
		df = df.set_index(self.col_pdv)

		self.__new_data = df

	#Fonction de supression d'action
	def supress_actions(self, action_ignore=["initialize_failed", "action_login", "login_failed", "initialize_success"]):
		df = self.data
		for ligne in action_ignore:
			df = df[df["nom_action"]!=ligne]
		df["n_id"] = [i for i in range(len(df))]
		df.set_index("n_id", inplace=True)
		df.reset_index()

	def get_new_data(self):
		return self.__new_data


if __name__=="__main__":
	path_data = ""
	df = pd.read_csv(path_data+"actionlog_week_202204150848.csv")
	transformedata = TransformDataPdv(df)
	transformedata.supress_actions()
	transformedata.liste_vecteurs_pdv()
	transformedata.construction_df()
	data_vect_pdv = transformedata.get_new_data()
	# stockage des points de ventes dans un fichier csv
	data_vect_pdv.to_csv(path_data+"vecteurs_pdv1.csv")

