from django.contrib import admin
from .models import produits, clients, fournisseurs, sorties,entrees,stock, smelting,refinering, fourcasterie,fourrafine

# Register your models here.
class clientsAdmin(admin.ModelAdmin):
    list_display = ('nom_clients', 'telephone')
admin.site.register(clients,clientsAdmin)

class produitsAdmin(admin.ModelAdmin):
    list_display = ('nomProdui','date_creation')
admin.site.register(produits,produitsAdmin)

class fournisseursAdmin(admin.ModelAdmin):
    list_display = ('nom_fournisseurs','telephone')
admin.site.register(fournisseurs,fournisseursAdmin)

class sortiesAdmin(admin.ModelAdmin):
    list_display = ('clients','produits','prix_vente','quantite','teneur','tvaPourcentage','date_sortie','prix_total')
admin.site.register(sorties,sortiesAdmin)

class entreesAdmin(admin.ModelAdmin):
    list_display = ('fournisseurs','produits','prix_achat','quantite','teneur','numero_tag','tvaPourcentage','date_sortie','prix_total')
admin.site.register(entrees,entreesAdmin)

class stockAdmin(admin.ModelAdmin):
    list_display = ('montant','produits')
admin.site.register(stock,stockAdmin)

class smeltingAdmin(admin.ModelAdmin):
    list_display = ('produits','fourcasterie','quantite_entrer','quantite_out','teneur_entrer','entrants','date_entrer')
admin.site.register(smelting,smeltingAdmin)

class refineringAdmin(admin.ModelAdmin):
    list_display = ('produits','fourrafine','quantite_entree','quantite_sortie','teneur_sortie','entrants','date_sortie')
admin.site.register(refinering,refineringAdmin)

class fourcasterieAdmin(admin.ModelAdmin):
    list_display = ('libelle','date_create')
admin.site.register(fourcasterie,fourcasterieAdmin)

class fourrafineAdmin(admin.ModelAdmin):
    list_display = ('libelle','date_create')
admin.site.register(fourrafine,fourrafineAdmin)



