from django.urls import path
from django.contrib.auth.decorators import login_required
from main_app.views import (UploadView, PreprocessView, AfficheDataView, 
	ConnexionView, InscriptionView, AdaptationDataView, TelechargerView,
    SegmentationView, DownloadSegmentView, EnvoiSegmentView, AccueilView)


urlpatterns = [
    path('', AccueilView.as_view(), name=""),
	path('upload/', UploadView.as_view(), name="upload"),
    path('connexion/', ConnexionView.as_view(), name="connexion"),
    path('inscription/', InscriptionView.as_view(), name="inscription"),
    path('preprocess1/<int:id>/', PreprocessView.as_view(), name="preprocess1"),
    path('affichedata/<int:id>/', AfficheDataView.as_view(), name="affichedata"),
    path('adapte/<int:id>/', AdaptationDataView.as_view(), name="adapte"),
    path('segmentation/<int:id>/', SegmentationView.as_view(), name="segmentation"),
    path('telechargement/<int:id>/<int:nb_segment>/', DownloadSegmentView.as_view(), name="segmentation"),
    path('download_cluster/<int:id>/<int:segment>/', EnvoiSegmentView.as_view(), name="download_cluster"),

    path('download/', TelechargerView.as_view(), name="download"),
]



