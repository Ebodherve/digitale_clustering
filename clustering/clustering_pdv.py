#Ce module contient les classes permettant de segmenter les points de ventes
#
#---------------------------------------------------------------------------#

import numpy as np
from scipy.spatial.distance import cdist
import pandas as pd

from clustering import preprocess_data


class KmeanClustering:

	def __init__(self, x, k, no_of_iterations=1000, distance='euclidean'):

		self.x = x
		self.k = k
		self.no_of_iterations = no_of_iterations
		self.distance = distance
		self.__clusters = None

	def entrainnement(self):
		x = self.x
		k = self.k
		distance = self.distance
		no_of_iterations = self.no_of_iterations
		if type(x)!=type(np.array([])):
			x = np.array(x)
		# Choix aléatoire des centroides
		idx = np.random.choice(len(x), k, replace=False)
		centroids = x[idx, :]

		# Calcule des distances de chaqu'exemple du jeux de données avec les centroides
		distances = cdist(x, centroids, distance)

		# Affectation des données aux differents cluster
		points = np.array([np.argmin(i) for i in distances])

		# Repetition du processus pour l'obtention des bons centres
		for _ in range(no_of_iterations):
			centroids = []
			for idx in range(k):
				# Calcule des nouveaux centres
				temp_cent = x[points==idx].mean(axis=0) 
				centroids.append(temp_cent)

			# Mise à jour des centres dans des tableaux numpy
			centroids = np.vstack(centroids)

			# Réaffectation des données aux différents centres
			distances = cdist(x, centroids ,distance)
			points = np.array([np.argmin(i) for i in distances])

		self.__clusters = points 

	def clusters(self):
		return self.__clusters


def culster_data_pdv(path_data, nb_of_clusters):
	#Lecture et transformation du jeux de données
	df = pd.read_csv(path_data)
	col_pdv = "pdv"
	transformedata = preprocess_data.TransformDataPdv(df, col_pdv=col_pdv)
	transformedata.supress_actions()
	transformedata.liste_vecteurs_pdv()
	transformedata.construction_df()
	data_vect_pdv = transformedata.get_new_data()

	#Application de l'algorithme kmean pour la segmentation des points de ventes
	pdv = data_vect_pdv.index
	kmeanpdv = KmeanClustering(data_vect_pdv, nb_of_clusters)
	kmeanpdv.entrainnement()

	#Arrangement des clusters dans un data frame
	clusters_pdv = kmeanpdv.clusters()
	clusters_pdv = pd.DataFrame({col_pdv:pdv, "classes":clusters_pdv})

	del data_vect_pdv
	del kmeanpdv

	return clusters_pdv


class ClusteringPdv:
	pass


if __name__=="__main__":

	path_data = ""
	culster_data_pdv(path_data+"actionlog_week_202204150848.csv", 10)


