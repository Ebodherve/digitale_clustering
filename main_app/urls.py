from django.urls import path
from django.contrib.auth.decorators import login_required
from main_app.views import (UploadView, PreprocessView, AfficheDataView, 
	ConnexionView, InscriptionView, AdaptationDataView, TelechargerView,
    SegmentationView, DownloadSegmentView, EnvoiSegmentView, AccueilView,
    VerificationDataView)


urlpatterns = [
    path('', AccueilView.as_view(), name=""),
	path('upload/', UploadView.as_view(), name="upload"),
    path('connexion/', ConnexionView.as_view(), name="connexion"),
    path('inscription/', InscriptionView.as_view(), name="inscription"),
    path('supp_vm/<int:id>/', PreprocessView.as_view(), name="supp_vm"),
    path('affichedata/<int:id>/', AfficheDataView.as_view(), name="affichedata"),
    path('adapte/<int:id>/', AdaptationDataView.as_view(), name="adapte"),
    path('verifi_data/<int:id>/', VerificationDataView.as_view(), name="verifi_data"),
    path('segmentation/<int:id>/', SegmentationView.as_view(), name="segmentation"),
    path('telechargement/<int:id>/<int:nb_segment>/', DownloadSegmentView.as_view(), name="segmentation"),
    path('download_cluster/<int:id>/<int:segment>/', EnvoiSegmentView.as_view(), name="download_cluster"),

    path('download/', TelechargerView.as_view(), name="download"),
]



