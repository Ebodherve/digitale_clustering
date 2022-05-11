"""segmentation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from main_app.views import UploadView, PreprocessView, AfficheData

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('envoi/', UploadView.as_view(), name="envoi"),
    path('preprocess1/<int:id>/', PreprocessView.as_view(), name="preprocess1"),
    path('affichedata/<int:id>/', AfficheData.as_view(), name="affichedata"),
]
