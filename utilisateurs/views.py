from django.views.decorators.csrf import csrf_protect
from django.shortcuts import redirect, render
from produits.views import accueil
from .adresse import IP_adress,pagevisiter,infoconnexion
from produits.models import Produits
from django.core.mail import send_mail
from .models import InformationsUtilisateurs,Utilisateurs,InfoConnexion,Commande,Article
from django.core.mail import EmailMessage


#Authentification d'un utilisateur
@csrf_protect
def login(request):
    a=pagevisiter(request,pk="page d'authentification")
    error=False
    if len(request.POST)>0:
        identifiant=request.POST['identifiant']
        password=request.POST['password']
        a=infoconnexion(request,identifiant,password)
        try:
            test=Utilisateurs.objects.get(adresse_mail=identifiant,password=password)
            request.session['utilisateur_id']=test.id
            return redirect('/accueil')
        except:
            error=True
            word="Entrez des informations correctes"
            return render(request,'login.html',locals())
    else:
        pass   
    return render(request,'login.html',locals())

#inscription d'un utilisateur
@csrf_protect
def inscription(request):
    a=pagevisiter(request,pk="page d'inscription")
    error_password=False
    error_adresse=False
    if len(request.POST)>0:
        nom=request.POST['nom']
        prenom=request.POST['prenom']
        adresse_mail=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']
        number=request.POST['phone']
        age=request.POST['age']
        quartier=request.POST['localisation']
        if 'adresse_ip' in request.session:
            adresse_ip = request.session['adresse_ip']
            adresse_ip=InformationsUtilisateurs.objects.get(id=adresse_ip)
        else:
            id=IP_adress(request)
            adresse_ip=InformationsUtilisateurs.objects.get(id=id)

        #Vérification de la correspondance des deux mots de passe

        #Si cela ne correspondent pas retourne erreur
        if password1 != password2:
            error_password=True
            erreur1="Les deux mots de passe ne correspondent pas"
            return render(request,'inscription.html',locals())

        #Si les deux mots de passe correspondent autre vérification
        else:
            test=Utilisateurs.objects.filter(adresse_mail=adresse_mail)
            #Vérification si l'adresse mail est déja lié à un compte
            if len(test)==1 or len(test)>1:
                error_adresse=True
                erreur2="Adresse email déjà liée à un compte"
                return render(request,'inscription.html',locals())
            else:
                user=Utilisateurs(
                    adresse_ip=adresse_ip,
                    nom=nom,
                    prenom=prenom,
                    adresse_mail=adresse_mail,
                    password=password1,
                    numero_tel=number,
                    localisation=quartier,
                    annee_naissance=2021-int(age)
                )
                user.save()
                return redirect('/connexion')
    else:
        return render(request,'inscription.html')

#Réiniatiliser un mot de passe
@csrf_protect
def reinitialiser(request):
    a=pagevisiter(request,pk="page de reinitialisation de mot de passe")
    error=False
    if len(request.POST)>0:
        email=request.POST['email']
        test=Utilisateurs.objects.filter(adresse_mail=email)
        if len(test)==1:
            code=12000
            email = EmailMessage(
                    'Hello',
                    'Body goes here',
                    'mbobeboris1@gmail.com',
                    ['mbobeboris1@gmail.com', 'mbobeboris1@gmail.com'],
                    ['mbobeboris1@gmail.com'],
                    reply_to=['mbobeboris1@gmail.com'],
                    headers={'Message-ID': 'foo'},
                )
            return redirect('/connexion')
        else:
            error=True
            erreur="Cette adresse mail n'est pas liée à un compte"
            return render(request,'reinitialiser.html',locals())
    else:
        return render(request,'reinitialiser.html')


def facture(request,pk):
    a=pagevisiter(request,pk="Page facture")
    commande=Commande.objects.get(id=pk)
    if 'utilisateur_id' in request.session:
        utilisateur_id = request.session['utilisateur_id']
        utilisateur=Utilisateurs.objects.get(id=utilisateur_id)
        article=Article.objects.filter(commande=commande)
        prix=0
        for i in article:
            prix=prix+i.prix*i.quantite
        return render(request,'facture.html',locals())
    else:
        return redirect('/connexion')

def profil(request):
    if 'utilisateur_id' in request.session:
        utilisateur_id=request.session['utilisateur_id']
        utilisateur=Utilisateurs.objects.get(id=utilisateur_id)
        commande=Commande.objects.filter(auteur=utilisateur)
    return render(request,'profil.html',locals())