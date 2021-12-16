from django.http import response
from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Produits,Categorie,SuperCategorie,ProduitsSuper
from datetime import datetime
from django.views.decorators.csrf import csrf_protect
from utilisateurs.adresse import IP_adress,creerCommande,ajouterProduits,creerCommande,pagevisiter,infoconnexion,enregistrer,savemessage, saveproduits
from utilisateurs.models import Utilisateurs,Message,ProduitsAjouter,InformationsUtilisateurs,Recherche,Commande,Article

# Create your views here.

@csrf_protect
def accueil(request):
    connect=False
    a=pagevisiter(request,pk="page_accueil")
    nombre,utilisateur=0,0
    image1=SuperCategorie.objects.get(id=1)
    image3=Categorie.objects.get(id=14)
    image4=Categorie.objects.get(id=4)
    image5=Categorie.objects.get(id=5)
    image6=Categorie.objects.get(id=6)
    image7=Categorie.objects.get(id=7)
    image8=Categorie.objects.get(id=8)
    image9=Categorie.objects.get(id=9)
    image10=Categorie.objects.get(id=10)
    image11=Categorie.objects.get(id=11)
    image12=Categorie.objects.get(id=12)
    image2=Categorie.objects.get(id=13)
    if 'utilisateur_id' in request.session:
        connect=True
        utilisateur_id = request.session['utilisateur_id']
        utilisateur=Utilisateurs.objects.get(id=utilisateur_id)
    if len(request.POST)>0:
        nom=request.POST['nom']
        email=request.POST['email']
        phone=request.POST['phone']
        message=request.POST['message']
        save=savemessage(request,connect,message,utilisateur,nom,email,phone)
        return redirect('/accueil')
    else:
        if 'commande_id' in request.session:
            commande_id = request.session['commande_id']
            commande=Commande.objects.get(id=commande_id)
            compte=Article.objects.filter(commande=commande)
            for i in compte:
                nombre=nombre+1
        else:
            nombre=0
    return render(request,'accueil.html',locals())
    
@csrf_protect
def categorie(request,pk):
    categorie=Categorie.objects.get(id=pk)
    produit=Produits.objects.filter(nom_categorie=categorie)
    request.session['categorie_id']=pk
    nombre=0
    if len(request.POST)>0:
        nom=request.POST['recherche']
        #Enregistrement de la recherche
        a=enregistrer(request,nom=nom,categorie=categorie)
        produit=Produits.objects.all().filter(nom_produit__icontains=nom)
        return render(request,'categories.html',locals())
    else:
        if 'commande_id' in request.session:
            commande_id = request.session['commande_id']
            commande=Commande.objects.get(id=commande_id)
            compte=Article.objects.filter(commande=commande)
            for i in compte:
                nombre=nombre+1
        else:
            nombre=0
    return render(request,'categories.html',locals())

def offre(request,pk):
    categorie=SuperCategorie.objects.get(id=pk)
    produit=ProduitsSuper.objects.filter(supercategorie=categorie)
    nombre=0
    if 'commande_id' in request.session:
        commande_id = request.session['commande_id']
        commande=Commande.objects.get(id=commande_id)
        compte=Article.objects.filter(commande=commande)
        for i in compte:
            nombre=nombre+1
    else:
        nombre=0
    return render(request,'offre.html',locals())
    
def ajout_panier(request,pk,prix):
    product=Produits.objects.get(id=pk)
    ajout=ajouterProduits(request,product,prix)
    if 'categorie_id' in request.session:
        categorie_id=request.session['categorie_id']
        categorie=Categorie.objects.get(id=categorie_id)
        products=Produits.objects.all()
        #for cart counter, fetching products ids added by customer from cookies
        response = redirect('/categorie/'+str(categorie_id))
        #adding product id to cookies
        if 'product_ids' in request.COOKIES:
            product_ids = request.COOKIES['product_ids']
            if product_ids=="":
                product_ids=str(pk)
            else:
                product_ids=product_ids+"|"+str(pk)
                
            response.set_cookie('product_ids', product_ids)
        else:
            response.set_cookie('product_ids', pk)

        #sauvegarde des besoins
        save=pagevisiter(request,pk="Ajouter au panier produits:{}".format(product))
        save2=saveproduits(request,product)

        messages.info(request,product.nom_produit+ " a été ajouté au panier!")
        return response
    else:
        return redirect('/accueil')

@csrf_protect
def panier(request):
    a=pagevisiter(request,pk="Page panier")
    if 'commande_id' in request.session:
        commande_id = request.session['commande_id']
        commande=Commande.objects.get(id=commande_id)
        produits=Article.objects.filter(commande=commande)
        prix=0
        for i in produits:
            prix=prix+i.prix*i.quantite
    if len(request.POST)>0:
        return redirect('/verification')
    else:
        pass
    return render(request,'panier.html',locals())

@csrf_protect
def verification(request):
    a=pagevisiter(request,pk="page de verification de compte")
    error=False
    verification=False
    if 'utilisateur_id' in request.session:
        utilisateur_id = request.session['utilisateur_id']
        utilisateur=Utilisateurs.objects.get(id=utilisateur_id)
        if 'commande_id' in request.session:
            if len(request.POST)>0:
                password=request.POST['password']
                if password==utilisateur.password:
                    commande_id = request.session['commande_id']
                    commande=Commande.objects.get(id=commande_id)
                    commande.auteur=utilisateur
                    commande.date_validation=datetime.now()
                    commande.valide=True
                    commande.save()
                    numero_facture=Commande.objects.get(id=commande_id)
                    a=supprimercookie(request)
                    b=creerCommande(request)
                    return redirect('/factures/'+str(numero_facture))
                else:
                    verification=True
                    error=True
                    erreur="Le mot de passe est incorrect"
                    return render(request,'confirmer.html',locals())
            else:
                return render(request,'confirmer.html',locals())
        else:
            return redirect('/accueil')
    else:
        if len(request.POST)>0:
            identifiant=request.POST['identifiant']
            password=request.POST['password']
            a=infoconnexion(request,identifiant,password)
            try:
                test=Utilisateurs.objects.get(adresse_mail=identifiant,password=password)
                request.session['utilisateur_id']=test.id
                return redirect('/panier')
            except:
                error=True
                word="Entrez des informations correctes"
                return render(request,'connexion.html',locals())
        else: 
            pass
    return render (request,'connexion.html',locals())


def supprimer(request,pk):
    objects=Produits.objects.get(id=pk)
    a=pagevisiter(request,pk="Suppression du produit {}".format(objects))
    return redirect('/supprimerarticle/'+str(pk))

def supprimercookie(request):
    if 'commande_id' in request.session:
        del request.session['commande_id']
    if 'produits_id' in request.session:
        del request.session['produits_id']
    return True


def description1(request,pk):
    produits=Produits.objects.get(id=pk)
    a=pagevisiter(request,pk="description 1 du produits {}".format(produits))
    return render(request,'description1.html',locals())

def description2(request,pk):
    produits=Produits.objects.get(id=pk)
    a=pagevisiter(request,pk="description 2 du produits {}".format(produits))
    return render(request,'description2.html',locals())

def description3(request,pk):
    produits=Produits.objects.get(id=pk)
    a=pagevisiter(request,pk="description 3 du produits {}".format(produits))
    return render(request,'description3.html',locals())

def description4(request,pk):
    produits=Produits.objects.get(id=pk)
    a=pagevisiter(request,pk="description 4 du produits {}".format(produits))
    return render(request,'description4.html',locals())

def description5(request,pk):
    produits=Produits.objects.get(id=pk)
    a=pagevisiter(request,pk="description 5 du produits {}".format(produits))
    return render(request,'description5.html',locals())

def handler404(request,*args,**argv):
    return redirect('/accueil')