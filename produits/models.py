from django.db import models
from django.contrib import admin

# Create your models here.


class Categorie(models.Model):
    nom=models.CharField(max_length=100)
    image_couverture=models.ImageField(upload_to='images_couvertures/')
    def __str__(self):
        return self.nom

class CategorieAdmin(admin.ModelAdmin):
    list_display=['nom']


class Produits(models.Model):
    nom_categorie=models.ForeignKey(Categorie,on_delete=models.CASCADE)
    nom_produit=models.CharField(max_length=90)
    description=models.TextField()
    prix=models.IntegerField()
    reduction=models.IntegerField(null=True,blank=True)
    quantite=models.IntegerField()
    photo1=models.ImageField(upload_to='images_produits/')
    photo2=models.ImageField(upload_to='images_produits/')
    photo3=models.ImageField(upload_to='images_produits/')
    photo4=models.ImageField(upload_to='images_produits/')
    photo5=models.ImageField(upload_to='images_produits/')

    def __str__(self):
        return "Catégorie:{} ,nom={},et prix={}".format(self.nom_categorie,self.nom_produit,self.prix)

class ProduitsAdmin(admin.ModelAdmin):
    list_display=['nom_categorie','nom_produit','prix']

class SuperCategorie(models.Model):
    nom=models.CharField(max_length=100)
    image_couverture=models.ImageField(upload_to='images_couvertures/')

class SuperCategorieAdmin(admin.ModelAdmin):
    list_display=['nom']

class ProduitsSuper(models.Model):
    supercategorie=models.ForeignKey(SuperCategorie,on_delete=models.CASCADE)
    produits=models.ForeignKey(Produits,on_delete=models.CASCADE)
    prix_promo=models.IntegerField()

class ProduitsSuperAdmin(admin.ModelAdmin):
    list_display=['supercategorie','prix_promo','produits']