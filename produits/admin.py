from django.contrib import admin
from .models import SuperCategorie,ProduitsSuper,ProduitsSuperAdmin,SuperCategorieAdmin,Categorie,CategorieAdmin,Produits,ProduitsAdmin
# Register your models here.

admin.site.register(Categorie,CategorieAdmin)
admin.site.register(SuperCategorie,SuperCategorieAdmin)
admin.site.register(Produits,ProduitsAdmin)
admin.site.register(ProduitsSuper,ProduitsSuperAdmin)