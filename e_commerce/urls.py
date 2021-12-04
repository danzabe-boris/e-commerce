"""e_commerce URL Configuration

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
from produits.views import accueil,supprimer,offre,verification,categorie,ajout_panier,panier,description1,description2,description3,description4,description5
from utilisateurs.views import login,profil,inscription,reinitialiser,facture
from utilisateurs.adresse import supprimerarticle,incrementer,decrementer
from django.conf.urls import handler404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('factures/<int:pk>', facture,name='facture'),
    path('accueil/',accueil,name='accueil'),
    path('categorie/<int:pk>', categorie,name='categorie'),
    path('ajout/<int:pk>/<int:prix>', ajout_panier,name='ajout'),
    path('panier', panier,name='panier'),
    path('connexion', login,name='connecter'),
    path('verification', verification,name='verification'),
    path('inscription', inscription,name='inscription'),
    path('reinitialiser', reinitialiser,name='reinitialiser'),
    path('description1/<int:pk>', description1,name='description1'),
    path('description2/<int:pk>', description2,name='description2'),
    path('description3/<int:pk>', description3,name='description3'),
    path('description4/<int:pk>', description4,name='description4'),
    path('description5/<int:pk>', description5,name='description5'),
    path('incrementer/<int:pk>', incrementer,name='incrementer'),
    path('decrementer/<int:pk>', decrementer,name='decrementer'),
    path('supprimerarticle/<int:pk>', supprimerarticle,name='supprimerarticle'),
    path('supprimer/<int:pk>', supprimer,name='supprimer'),
    path('offre/<int:pk>', offre,name='offre'),
    path('profil', profil,name='profil'),

]
handler404='produits.views.handler404'
