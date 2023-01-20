from django.contrib import admin
from .models import produits, clients, fournisseurs, sorties,entrees,stock, fourcasterie,fourrafine,users,depanses,commande,transformations

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
    list_display = ('clients',
    'produits',
    'quantite_en_kg',
    'prix_vente_en_dollard',
    'teneur_en_pourcentage',
    'date_sortie',
    'prix_total_en_dollard','user')
admin.site.register(sorties,sortiesAdmin)
class DepansesInline(admin.TabularInline):
    model = entrees.depanses.through
class entreesAdmin(admin.ModelAdmin):
    # filter_vertical = ('depanses',)
    # inlines = (DepansesInline,)
    list_display = ('user',
    'fournisseurs','produits',
    'quantite_en_kg','prix_achat_en_dollard',
    'depense_list','montant_depanses_en_dollard',
    'descriptions','prix_total_en_dollard',
    'teneur_en_pourcentage','numero_tag',
    'source_minier','date_entrer')
    def depense_list(self, obj):
        return ",".join([depanse.name for depanse in  obj.depanses.order_by("name") ])
    depense_list.short_description = "depanse"
admin.site.register(entrees,entreesAdmin)

class stockAdmin(admin.ModelAdmin):
    list_display = ('montant','produits')
admin.site.register(stock,stockAdmin)

# class smeltingAdmin(admin.ModelAdmin):
#     list_display = ('produits','fourcasterie','quantite_entrer','quantite_out','teneur_entrer','entrants','date_entrer','user')
# admin.site.register(smelting,smeltingAdmin)

# class refineringAdmin(admin.ModelAdmin):
#     list_display = ('produits','fourrafine','quantite_sortie','teneur_sortie','entrants','date_sortie','user')
# admin.site.register(refinering,refineringAdmin)
class transformationsAdmin(admin.ModelAdmin):
    pass
    list_display = ('user',
    'produits',
    'fourcasterie',
    'fourrafine',
    'quantite_entrer_casterie_en_kg',
    'quantite_sortie_casterie_en_kg',
    'quantite_entrer_etain_en_kg',
    'quantite_sortie_etain_en_kg',
    'entrant_casterie_en_kg',
    'entrant_etain_en_kg',
    'teneur_casterie_en_pourcentage',
    'teneur_etain_en_pourcentage',
    'date_entrer',
    'date_sortie')
admin.site.register(transformations,transformationsAdmin)

class fourcasterieAdmin(admin.ModelAdmin):
    list_display = ('libelle','date_create')
admin.site.register(fourcasterie,fourcasterieAdmin)

class fourrafineAdmin(admin.ModelAdmin):
    list_display = ('libelle','date_create')
admin.site.register(fourrafine,fourrafineAdmin)
class usersAdmin(admin.ModelAdmin):
    list_display = ('user','name','post_nom','ville','matricule','telephone','email','image_pic')
admin.site.register(users,usersAdmin)

class depansesAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(depanses,depansesAdmin)

class commandeAdmin(admin.ModelAdmin):
    list_display = ('produits','clients','status','prix_vente','quantite','teneur','date_commander','date_modifier','prix_total')
admin.site.register(commande,commandeAdmin)


