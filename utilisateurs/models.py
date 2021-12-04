from django.db import models
from django.contrib import admin
from produits.models import Categorie,Produits

# Create your models here.
class InformationsUtilisateurs(models.Model):
    adresse_ip=models.CharField(max_length=1000)
    valide=models.CharField(max_length=100)
    ville=models.CharField(max_length=100)
    code_continent=models.CharField(max_length=10)
    nom_continent=models.CharField(max_length=100)
    code_pays=models.CharField(max_length=10)
    nom_pays=models.CharField(max_length=100)
    union_europeene=models.CharField(max_length=100)
    latitude=models.CharField(max_length=100)
    longitude=models.CharField(max_length=100)
    code_postal=models.CharField(max_length=100)
    zone_horaire=models.CharField(max_length=100)

    def __str__(self):
        return self.adresse_ip

class InformationsAdmin(admin.ModelAdmin):
    list_display=['adresse_ip','valide','ville','nom_continent','nom_pays','latitude','longitude']


class Utilisateurs(models.Model):
    adresse_ip=models.ForeignKey(InformationsUtilisateurs,on_delete=models.CASCADE)
    nom=models.CharField(max_length=100)
    prenom=models.CharField(max_length=100)
    adresse_mail=models.EmailField()
    password=models.CharField(max_length=100)
    numero_tel=models.IntegerField()
    annee_naissance=models.IntegerField()
    localisation=models.CharField(max_length=1000)

    def __str__(self):
        return "{} {}".format(self.adresse_ip,self.nom)

class UtilisateursAdmin(admin.ModelAdmin):
    list_display=['nom','prenom','password','adresse_mail','numero_tel','localisation']

class Message(models.Model):
    adresse_ip=models.ForeignKey(InformationsUtilisateurs,on_delete=models.CASCADE,null=True)
    auteur=models.ForeignKey(Utilisateurs,on_delete=models.CASCADE,null=True)
    nom_saisi=models.CharField(max_length=1000)
    email_saisi=models.EmailField()
    phone=models.IntegerField()
    messages=models.TextField()
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} {}".format(self.adresse_ip,self.messages)

class MessageAdmin(admin.ModelAdmin):
    list_display=['adresse_ip','auteur','nom_saisi','email_saisi','phone','messages','date']

class InfoConnexion(models.Model):
    test_email=models.EmailField()
    test_password=models.CharField(max_length=1000)
    date=models.DateTimeField(auto_now_add=True)
    adresse_ip=models.ForeignKey(InformationsUtilisateurs,on_delete=models.CASCADE)

class InfoConnexionAdmin(admin.ModelAdmin):
    list_display=['test_email','test_password','adresse_ip','date']

class Recherche(models.Model):
    auteur=models.ForeignKey(Utilisateurs,on_delete=models.CASCADE,null=True)
    adresse_ip=models.ForeignKey(InformationsUtilisateurs,on_delete=models.CASCADE,null=True)
    nom_recherche=models.CharField(max_length=100)
    date=models.DateTimeField(auto_now_add=True)
    categorie_recherche=models.ForeignKey(Categorie,on_delete=models.CASCADE)

class RechercheAdmin(admin.ModelAdmin):
    list_display=['adresse_ip','auteur','nom_recherche','categorie_recherche','date']

class ProduitsAjouter(models.Model):
    auteur=models.ForeignKey(Utilisateurs,on_delete=models.CASCADE,null=True)
    adresse_ip=models.ForeignKey(InformationsUtilisateurs,on_delete=models.CASCADE,null=True)
    produits=models.ForeignKey(Produits,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)

class ProduitsAjouterAdmin(admin.ModelAdmin):
    list_display=['adresse_ip','auteur','produits','date']

class ProduitsSupprimer(models.Model):
    auteur=models.ForeignKey(Utilisateurs,on_delete=models.CASCADE,null=True)
    adresse_ip=models.ForeignKey(InformationsUtilisateurs,on_delete=models.CASCADE,null=True)
    produits=models.ForeignKey(Produits,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)

class ProduitsSupprimerAdmin(admin.ModelAdmin):
    list_display=['adresse_ip','auteur','produits','date']

class PageVisiter(models.Model):
    auteur=models.ForeignKey(Utilisateurs,on_delete=models.CASCADE,null=True)
    adresse_ip=models.ForeignKey(InformationsUtilisateurs,on_delete=models.CASCADE,null=True)
    page=models.CharField(max_length=100)
    date=models.DateTimeField(auto_now_add=True)

class PageVisiterAdmin(admin.ModelAdmin):
    list_display=['adresse_ip','auteur','page','date']

class Commande(models.Model):
    auteur=models.ForeignKey(Utilisateurs,on_delete=models.CASCADE,null=True)
    date=models.DateTimeField(auto_now_add=True)
    date_validation=models.DateTimeField(null=True)
    valide=models.BooleanField(default=False)
    def __str__(self):
        return str(self.id)

class CommandeAdmin(admin.ModelAdmin):
    list_display=['auteur','date','date_validation','valide']
    
class Article(models.Model):
    produits=models.ForeignKey(Produits,on_delete=models.CASCADE)
    quantite=models.IntegerField(default=1)
    prix=models.IntegerField(default=0)
    commande=models.ForeignKey(Commande,on_delete=models.CASCADE)

class ArticleAdmin(admin.ModelAdmin):
    list_display=['produits','quantite','commande']