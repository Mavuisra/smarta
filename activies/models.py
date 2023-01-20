from django.db import models
from django.contrib.auth.models import User
import statistics
import datetime


class commande(models.Model):
    STATUS = (
('livree','livree'),
('non_livree','non_livree')
    )

    produits = models.ForeignKey("produits", on_delete = models.CASCADE)
    clients = models.ForeignKey("clients", on_delete = models.CASCADE, related_name = 'client')
    status = models.CharField(max_length = 20, choices=STATUS)
    prix_vente = models.FloatField( default=0.0)
    quantite = models.FloatField(default=0.0)
    teneur = models.FloatField(default=0.0)
    date_commander = models.DateTimeField(auto_now_add=True)
    date_modifier = models.DateTimeField(auto_now=True)
    prix_total = models.FloatField(default=0.0)
    
    def __str__(self) :
        return self.produits.nomProdui
    

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

class users(models.Model):
    user = models.OneToOneField(User, null=True, blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length = 20)
    post_nom =models.CharField(max_length = 20)
    ville =models.CharField(max_length = 20) 
    matricule = models.CharField(max_length = 20)
    telephone = models.CharField(max_length = 20)
    email =models.CharField(max_length = 20)
    image_pic = models.ImageField(null = True, blank=True, default='media/prof.jpeg', upload_to='media') 
    date_created = models.DateTimeField(default= datetime.datetime.today())
    def __str__(self) :
        return self.name

class sorties(models.Model):
    user = models.ForeignKey(users, null=True, blank=True,on_delete=models.SET_NULL)
    clients = models.ForeignKey("clients", on_delete = models.CASCADE, related_name = 'clients')
    produits = models.ForeignKey("produits", on_delete = models.CASCADE, related_name = 'produit')
    quantite_en_kg = models.FloatField(default=0.0, null=False)
    prix_vente_en_dollard = models.FloatField(default=0.0, null=False)
    teneur_en_pourcentage = models.FloatField(default=0.0, null=False)
    # tvaPourcentage = models.FloatField(default=0.0, null=False)
    date_sortie  =  models.DateTimeField(auto_now=True)
    prix_total_en_dollard = models.FloatField(default=0.0)
    class Meta():
        ordering = ['-date_sortie']

class entrees(models.Model):
    user = models.ForeignKey(users, null=True, blank=True, on_delete=models.CASCADE)
    fournisseurs = models.ForeignKey("fournisseurs", on_delete = models.CASCADE)
    numero_tag = models.CharField(max_length = 20)
    source_minier = models.CharField(max_length=200, null=True)
    produits = models.ForeignKey("produits", on_delete = models.CASCADE)
    teneur_en_pourcentage = models.FloatField(default=0.0, null = False)
    quantite_en_kg = models.FloatField( default=0.0, null = False)
    prix_achat_en_dollard = models.FloatField(default=0.0, null = False)
    prix_total_en_dollard = models.FloatField(default=0.0)
    montant_depanses_en_dollard  = models.FloatField(null=True, default = 0.0)
    depanses = models.ManyToManyField("depanses",)
    descriptions = models.TextField(max_length = 200, null=True)
    date_entrer =  models.DateTimeField(auto_now = True)
    # date_entrer  =  models.DateTimeField(auto_now =True, default= datetime.datetime.now())
    class Meta():
        ordering = ['-date_entrer']
class depanses(models.Model):
    name = models.CharField(max_length=222, default='', null=True)
    def __str__(self) :
        return self.name

class stock(models.Model):
    montant = models.FloatField()
    produits =  models.ForeignKey("produits", on_delete = models.CASCADE)


class transformations(models.Model):
    user = models.ForeignKey(users, null=True, blank=True,on_delete=models.SET_NULL)
    produits =  models.ForeignKey("produits", on_delete = models.CASCADE)
    fourcasterie = models.ForeignKey("fourcasterie", on_delete = models.CASCADE)
    fourrafine = models.ForeignKey("fourrafine", on_delete = models.CASCADE, null=True)
    quantite_entrer_casterie_en_kg = models.FloatField( default = 0.0 )
    quantite_sortie_casterie_en_kg = models.FloatField( default = 0.0 )
    quantite_entrer_etain_en_kg = models.FloatField( default = 0.0 )
    quantite_sortie_etain_en_kg = models.FloatField( default = 0.0 )
    entrant_casterie_en_kg = models.FloatField( default = 0.0 )
    entrant_etain_en_kg = models.FloatField( default = 0.0 )
    teneur_casterie_en_pourcentage = models.FloatField( default = 0.0 )
    
    teneur_etain_en_pourcentage = models.FloatField( default = 0.0 ) 
    date_entrer =  models.DateTimeField(auto_now_add = True)
    date_sortie =  models.DateTimeField(auto_now = True)


class fourcasterie(models.Model):
    libelle = models.CharField(max_length = 255,default = 'SF')
    date_create  =  models.DateTimeField(auto_now = True)

    def __str__(self) :
        return self.libelle

class fourrafine(models.Model):
    libelle = models.CharField(max_length = 255, default = 'null')
    date_create = models.DateTimeField(auto_now = True)

    def __str__(self) :
        return self.libelle







    





