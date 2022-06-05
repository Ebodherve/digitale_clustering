from django.urls import path
from main_app.views import *
from django.contrib.auth.decorators import login_required
from main_app.views import (UploadView, PreprocessView, AfficheDataView, 
	ConnexionView, InscriptionView, AdaptationDataView, TelechargerView)


urlpatterns = [
	path('envoi/', UploadView.as_view(), name="envoi"),
    path('connexion/', ConnexionView.as_view(), name="connexion"),
    path('inscription/', InscriptionView.as_view(), name="inscription"),
    path('preprocess1/<int:id>/', PreprocessView.as_view(), name="preprocess1"),
    path('affichedata/<int:id>/', AfficheDataView.as_view(), name="affichedata"),
    path('adapte/<int:id>/', AdaptationDataView.as_view(), name="adapte"),
    path('download/', TelechargerView.as_view(), name="download"),
]



