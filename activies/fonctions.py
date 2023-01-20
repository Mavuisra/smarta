import numpy as np
from .models import *
from django.db.models import Sum, Avg, Count
from django.contrib import messages
class myClasses:
    
    def moyenne_teneur(self):
        all_achats = entrees.objects.all().values()
        quantite_list = []
        teneur_list = []
        
        for all_achat in all_achats:
            quantite = all_achat["quantite_en_kg"]
            teneur = all_achat["teneur_en_pourcentage"]
            quantite_list.append(quantite)
            teneur_list.append(teneur)
        print(quantite_list)
        print(teneur_list)
        somme_quantite_teneur = np.sum(np.multiply(quantite_list ,teneur_list))
        somme_quantite = np.sum(quantite_list)
        moyenne_teneur = somme_quantite_teneur / somme_quantite
        return moyenne_teneur
    def moyenne_teneur_etain(self):
        all_achats = transformations.objects.all().values()
        quantite_list = []
        teneur_list = []
        
        for all_achat in all_achats:
            quantite = all_achat["quantite_sortie_etain_en_kg"]
            teneur = all_achat["teneur_etain_en_pourcentage"]
            quantite_list.append(quantite)
            teneur_list.append(teneur)
        print(quantite_list)
        print(teneur_list)
        somme_quantite_teneur = np.sum(np.multiply(quantite_list ,teneur_list))
        somme_quantite = np.sum(quantite_list)
        moyenne_teneur = somme_quantite_teneur / somme_quantite
        return moyenne_teneur
    def stock_casterie(self):

        stock_casterie = None
        all_stats= []
        all_achats = entrees.objects.all().filter(produits_id = 5)
        all_ventes = sorties.objects.all().filter(produits_id = 5)
        all_transformations = transformations.objects.all()
        all_commande = commande.objects.all().filter(produits_id = 5, status = "livree")

        s_qt_vente = all_ventes.aggregate(Sum('quantite_en_kg'))['quantite_en_kg__sum']
        s_qt_achats = all_achats.aggregate(Sum('quantite_en_kg'))['quantite_en_kg__sum']
        s_qt_transformer = all_transformations.aggregate(Sum('quantite_entrer_casterie_en_kg'))['quantite_entrer_casterie_en_kg__sum']
        s_qt_livree = all_commande.aggregate(Sum('quantite'))['quantite__sum']
        if (s_qt_achats is not None and s_qt_vente is not None and s_qt_transformer is not None and s_qt_livree is not None):
            if s_qt_achats > (s_qt_achats - s_qt_vente - s_qt_transformer - s_qt_livree):
                stock_casterie = s_qt_achats - s_qt_vente - s_qt_transformer - s_qt_livree
        return stock_casterie 
    def stock_etain(self):

        stock_etain = None
        all_ventes = sorties.objects.all().filter(produits_id = 6)
        all_transformations = transformations.objects.all()
        all_commande = commande.objects.all().filter(produits_id = 6, status = "livree")

        s_qt_vente = all_ventes.aggregate(Sum('quantite_en_kg'))['quantite_en_kg__sum']
        s_qt_transformer = all_transformations.aggregate(Sum('quantite_sortie_etain_en_kg'))['quantite_sortie_etain_en_kg__sum']
        s_qt_livree = all_commande.aggregate(Sum('quantite'))['quantite__sum']
        if (s_qt_transformer is not None and s_qt_vente is not None and s_qt_livree is not None):
            if s_qt_transformer > ( s_qt_vente  - s_qt_livree):
                stock_etain = s_qt_transformer - s_qt_vente  - s_qt_livree
            else:
                stock_etain = 'not inferieur'
                return stock_etain 
        else:
            stock_etain = s_qt_transformer - s_qt_vente  

            return stock_etain 
            
        return stock_etain
    def stats_all(self):
        stock_casterie = None
        all_stats={}
        all_achats = entrees.objects.all().filter(produits_id = 5)
        all_ventes = sorties.objects.all().filter(produits_id = 6)

        all_transformations = transformations.objects.all()
        all_commande = commande.objects.all().filter(produits_id = 5, status = "livree")
        all_commandes = commande.objects.all().filter(produits_id = 5, status = "non_livree")

        all_commande_etain = commande.objects.all().filter(produits_id = 6, status = "livree")
        all_commandes_etain = commande.objects.all().filter(produits_id = 6, status = "non_livree")
        al_ventes_etain = sorties.objects.all().filter(produits_id = 6)

        s_qt_vente = all_ventes.aggregate(Sum('quantite_en_kg'))['quantite_en_kg__sum']
        s_qt_vente_vente = al_ventes_etain.aggregate(Sum('quantite_en_kg'))['quantite_en_kg__sum']
        s_qt_achats = all_achats.aggregate(Sum('quantite_en_kg'))['quantite_en_kg__sum']
        s_qt_transformer = all_transformations.aggregate(Sum('quantite_entrer_casterie_en_kg'))['quantite_entrer_casterie_en_kg__sum']

        s_qt_transformer_etain = all_transformations.aggregate(Sum('quantite_sortie_etain_en_kg'))['quantite_sortie_etain_en_kg__sum']
        s_qt_entrer_etain = all_transformations.aggregate(Sum('quantite_sortie_casterie_en_kg'))['quantite_sortie_casterie_en_kg__sum']

        s_qt_livree = all_commande.aggregate(Sum('quantite'))['quantite__sum']
        s_qt_non_livree = all_commandes.aggregate(Sum('quantite'))['quantite__sum']
        
        s_qt_livree_etain = all_commande_etain.aggregate(Sum('quantite'))['quantite__sum']
        s_qt_non_livree_etain = all_commandes_etain.aggregate(Sum('quantite'))['quantite__sum']
        all_stats = {
            's_qt_non_livree_etain':s_qt_non_livree_etain,
            's_qt_livree_etain':s_qt_livree_etain,
            's_qt_vente_vente':s_qt_vente_vente,
            's_qt_entrer_etain':s_qt_entrer_etain,
            's_qt_transformer_etain':s_qt_transformer_etain,
            's_qt_non_livree':s_qt_non_livree,
            's_qt_livree':s_qt_livree,
            'all_commandes_etain':all_commandes_etain,
            's_qt_non_livree':s_qt_non_livree,
            'somme_vente':s_qt_vente,
            'somme_achat':s_qt_achats,
            'somme_trans_cast':s_qt_transformer,
            'somme_livree_cast':s_qt_livree,

        }
        return all_stats
        
            


