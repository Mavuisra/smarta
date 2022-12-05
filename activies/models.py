from django.db import models
import statistics



# Create your models here.


class produits(models.Model):
    nomProdui = models.CharField(max_length = 20)
    date_creation = models.DateTimeField(auto_now = True)
    def __str__(self) :
        return self.nomProdui

class clients(models.Model):

    nom_clients = models.CharField(max_length = 50)
    sexe = models.CharField(max_length = 10, default= 'homme')
    telephone = models.CharField(max_length = 50)
    created_at  =  models.DateTimeField(auto_now = True)
    def __str__(self) :
        return self.nom_clients
    class Meta():
        ordering = ['-created_at']
class fournisseurs(models.Model):
 
    nom_fournisseurs = models.CharField(max_length = 50)
    sexe = models.CharField(max_length = 10, default= 'homme')
    telephone = models.CharField(max_length = 50)
    created_at  =  models.DateTimeField(auto_now = True)
    def __str__(self) :
        return self.nom_fournisseurs

class sorties(models.Model):
    
    clients = models.ForeignKey("clients", on_delete = models.CASCADE, related_name = 'clients')
    produits = models.ForeignKey("produits", on_delete = models.CASCADE, related_name = 'produit')
    prix_vente = models.DecimalField(max_digits = 8, decimal_places = 2)
    quantite = models.FloatField()
    teneur = models.DecimalField(max_digits = 8, decimal_places = 2)
    tvaPourcentage = models.FloatField(default= '0.0')
    date_sortie  =  models.DateTimeField(auto_now = True)
    prix_total = models.DecimalField(max_digits = 8, decimal_places = 2, default = 0.0)
    class Meta():
        ordering = ['-date_sortie']
           
   
class entrees(models.Model):
    fournisseurs = models.ForeignKey("fournisseurs", on_delete = models.CASCADE)
    produits = models.ForeignKey("produits", on_delete = models.CASCADE)
    prix_achat = models.FloatField()
    quantite = models.FloatField()
    teneur = models.DecimalField(max_digits = 8, decimal_places = 2)
    numero_tag = models.CharField(max_length = 20)
    tvaPourcentage = models.FloatField(max_length = 20, default = 0.0)
    date_sortie  =  models.DateTimeField(auto_now = True)
    prix_total = models.DecimalField(max_digits = 8, decimal_places = 2, default = 0.0)
    

class stock(models.Model):
    montant = models.FloatField()
    produits =  models.ForeignKey("produits", on_delete = models.CASCADE)

class smelting(models.Model):
    produits =  models.ForeignKey("produits", on_delete = models.CASCADE)
    fourcasterie = models.ForeignKey("fourcasterie", on_delete = models.CASCADE)
    quantite_entrer = models.FloatField(null = True, default = 0.0, blank = True)
    quantite_out = models.FloatField(null = True, default = 0.0, blank = True)
    teneur_entrer = models.DecimalField(max_digits = 8, decimal_places = 2)
    date_entrer =  models.DateTimeField(auto_now = True)
    entrants = models.FloatField(null = True, default = 0.0, blank = True)
class refinering(models.Model):
    produits = models.ForeignKey("produits", on_delete = models.CASCADE )
    fourrafine = models.ForeignKey("fourrafine", on_delete = models.CASCADE)
    quantite_entree = models.FloatField(null = True, default = 0.0, blank = True)
    quantite_sortie = models.FloatField(null = True, default = 0.0, blank = True)
    teneur_sortie = models.DecimalField(max_digits = 8, decimal_places = 2)
    date_sortie  =  models.DateTimeField(auto_now = True)
    entrants = models.FloatField(null = True, default = 0.0, blank = True);

class fourcasterie(models.Model):
    libelle = models.CharField(max_length = 255,default = 'SF')
    date_create  =  models.DateTimeField(auto_now = True)

    def __str__(self) :
        return self.libelle

class fourrafine(models.Model):
    libelle = models.CharField(max_length = 255, default = 'RF')
    date_create = models.DateTimeField(auto_now = True)

    def __str__(self) :
        return self.libelle







    





