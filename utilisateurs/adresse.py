import socket
from django.contrib.gis.geoip2 import GeoIP2
from django.shortcuts import render,redirect
from .models import InformationsUtilisateurs,Message,Article,Produits,Commande,InfoConnexion,Utilisateurs,PageVisiter,Recherche,ProduitsAjouter

def IP_adress(request):

    #L'obtention de l'adresse ip d'un usager du site
    ip=0
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    #Vérification si l'adresse ip est valide
    try:
        socket.inet_aton(ip)
        ip_valid = True
    except socket.error:
        ip_valid = False

    #Test de localisation de l'adresse ip avec GeoIp2
    g = GeoIP2()
    try:
        latitude=g.city(ip)
        ville=latitude["city"]
        continent_code=latitude["continent_code"]
        nom_continent=latitude["continent_name"]
        code_pays,region=latitude["country_code"],latitude["region"]
        nom_pays,temps=latitude["country_name"],latitude["time_zone"]
        union,code=latitude["is_in_european_union"],latitude["postal_code"]
        latitude,longitude=latitude["latitude"],latitude["longitude"]
        data=InformationsUtilisateurs(
            adresse_ip=ip,
            valide=ip_valid,
            ville=ville,
            code_continent=continent_code,
            nom_continent=nom_continent,
            code_pays=code_pays,
            nom_pays=nom_pays,
            union_europeene=union,
            latitude=latitude,
            longitude=longitude,
            code_postal=code,
            zone_horaire=temps
            )
        data.save()
        request.session['adresse_ip']=data.id
    except:
        data=InformationsUtilisateurs(
            adresse_ip=ip,
            valide=ip_valid,
            ville='inconnu',
            code_continent='inconnu',
            nom_continent='inconnu',
            code_pays='inconnu',
            nom_pays='inconnu',
            union_europeene='inconnu',
            latitude='inconnu',
            longitude='inconnu',
            code_postal='inconnu',
            zone_horaire='inconnu'
        )
        data.save()
        request.session['adresse_ip']=data.id
    return data.id

def pagevisiter(request,pk):
    nom_page=pk
    if 'utilisateur_id' in request.session:
            utilisateur_id = request.session['utilisateur_id']
            utilisateur=Utilisateurs.objects.get(id=utilisateur_id)
            test=PageVisiter(
                auteur=utilisateur,
                page=pk
                )
            test.save()
    elif 'adresse_ip' in request.session:
        adresse_ip=request.session['adresse_ip']
        adresseip=InformationsUtilisateurs.objects.get(id=adresse_ip)
        test=PageVisiter(
            adresse_ip=adresseip,
            page=pk
            )
        test.save()
    else:
        adresse=IP_adress(request)
        adresseip=InformationsUtilisateurs.objects.get(id=adresse)
        test=PageVisiter(
            adresse_ip=adresseip,
            page=pk
            )
        test.save()
    return True

def enregistrer(request,nom,categorie):

    if 'utilisateur_id' in request.session:
        utilisateur_id = request.session['utilisateur_id']
        utilisateur=Utilisateurs.objects.get(id=utilisateur_id)
        test=Recherche(
            auteur=utilisateur,
            nom_recherche=nom,
            categorie_recherche=categorie,
           )
        test.save()

    elif 'adresse_ip' in request.session:
        adresse_ip=request.session['adresse_ip']
        adresseip=InformationsUtilisateurs.objects.get(id=adresse_ip)
        test=Recherche(
            adresse_ip=adresseip,
            nom_recherche=nom,
            categorie_recherche=categorie,
            )
        test.save()

    else:
        adresse=IP_adress(request)
        adresseip=InformationsUtilisateurs.objects.get(id=adresse)
        test=Recherche(
        adresse_ip=adresseip,
        nom_recherche=nom,
        categorie_recherche=categorie,
            )
        test.save()

def savemessage(request,connect,message,utilisateur,nom,email,phone):
    if connect:
        message=Message(
            auteur=utilisateur,
            nom_saisi=nom,
            email_saisi=email,
            phone=phone,
            messages=message
            )
        message.save()
    elif 'adresse_ip' in request.session:
        adresse_ip= request.session['adresse_ip']
        adresseip=InformationsUtilisateurs.objects.get(id=adresse_ip)
        message=Message(
                adresse_ip=adresseip,
                nom_saisi=nom,
                email_saisi=email,
                phone=phone,
                messages=message
            )
        message.save()
    else:
        id=IP_adress(request)
        adresse_ip=InformationsUtilisateurs.objects.get(id=id)
        message=Message(
                adresse_ip=adresse_ip,
                nom_saisi=nom,
                email_saisi=email,
                phone=phone,
                messages=message
            )
        message.save()

def saveproduits(request,product):
    if 'utilisateur_id' in request.session:
        utilisateur_id = request.session['utilisateur_id']
        utilisateur=Utilisateurs.objects.get(id=utilisateur_id)
        test=ProduitsAjouter(auteur=utilisateur,
            produits=product
            )
        test.save()
    elif 'adresse_ip' in request.session:
        adresse_ip= request.session['adresse_ip']
        adresseip=InformationsUtilisateurs.objects.get(id=adresse_ip)
        test=ProduitsAjouter(adresse_ip=adresseip,
            produits=product
            )
        test.save()
    else:
        ip=IP_adress(request)
        adresseip=InformationsUtilisateurs.objects.get(id=ip)
        test=ProduitsAjouter(adresse_ip=adresseip,
           produits=product
            )
        test.save()

def infoconnexion(request,identifiant,password):
    if 'adresse_ip' in request.session:
        adresse_ip= request.session['adresse_ip']
        adresseip=InformationsUtilisateurs.objects.get(id=adresse_ip)
        test=InfoConnexion(
            test_email=identifiant,
            test_password=password,
            adresse_ip=adresseip,
            )
        test.save()
    else:
        test=IP_adress(request)
        adresse_ip=InformationsUtilisateurs.objects.get(id=test)
        test3=InfoConnexion(
                 test_email=identifiant,
                 test_password=password,
                 adresse_ip=adresse_ip,
                )
        test3.save()

def creerCommande(request):
    commande=Commande()
    commande.save()
    request.session['commande_id']=commande.id
    return commande.id

def ajouterProduits(request,produits,prix):
    if 'commande_id' in request.session:
        pass
    else:
        creer=creerCommande(request)
        
    if 'commande_id' in request.session:
        commande_id = request.session['commande_id']
        commande=Commande.objects.get(id=commande_id)
        objects=Article.objects.filter(commande=commande)
        if 'produits_id' in request.session:
            id=request.session['produits_id']
            if id==produits.id:
                pass
            else:
                article=Article(
                            commande=commande,
                            produits=produits,
                            quantite=1,
                            prix=prix
                                )
                article.save()
        else:
            article=Article(
                        commande=commande,
                        produits=produits,
                        quantite=1,
                        prix=prix
                        )
            article.save()
    else:
        commande=creerCommande(request)
        commande=Commande.objects.get(id=commande)
        if 'produits_id' in request.session:
            id=request.session['produits_id']
            if id==produits.id:
                pass
            else:
                article=Article(
                        commande=commande,
                        produits=produits,
                        quantite=1,
                        prix=prix
                            )
                article.save()
    request.session['produits_id']=produits.id
    return produits.id

def supprimerarticle(request,pk):
    produits=Produits.objects.get(id=pk)
    article=Article.objects.filter(produits=produits)
    article.delete()
    if 'produits_id' in request.session:
        del request.session['produits_id']
    return redirect('/panier')

def incrementer(request,pk):
    if 'commande_id' in request.session:
        commande_id = request.session['commande_id']
        commande=Commande.objects.get(id=commande_id)
        article=Article.objects.get(id=pk,commande=commande)
        article.quantite=article.quantite+1
        article.save()
    return redirect('/panier')
    
def decrementer(request,pk):
    if 'commande_id' in request.session:
        commande_id = request.session['commande_id']
        commande=Commande.objects.get(id=commande_id)
        article=Article.objects.get(id=pk,commande=commande)
        if article.quantite==1:
            pass
        else:
            article.quantite=article.quantite-1
            article.save()
    return redirect('/panier')