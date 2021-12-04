from django.contrib import admin
from .models import InformationsUtilisateurs,Commande,CommandeAdmin,Article,ArticleAdmin,PageVisiter,PageVisiterAdmin,Message,MessageAdmin,InformationsAdmin, Utilisateurs,UtilisateursAdmin,Recherche,RechercheAdmin
# Register your models here.

admin.site.register(InformationsUtilisateurs,InformationsAdmin)
admin.site.register(Utilisateurs,UtilisateursAdmin)
admin.site.register(Message,MessageAdmin)
admin.site.register(Recherche,RechercheAdmin)
admin.site.register(PageVisiter,PageVisiterAdmin)
admin.site.register(Article,ArticleAdmin)
admin.site.register(Commande,CommandeAdmin)