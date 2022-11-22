from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from .models import clients, entrees,sorties, produits, clients, smelting, fourcasterie, refinering, fourrafine,stock,fournisseurs
from django.db.models import Sum, Avg, Count
# Create your views here.

produit = produits.objects.all().values()
client = clients.objects.all().values()
fournisseur = fournisseurs.objects.all().values()

moyenne_teneur = entrees.objects.aggregate(Avg('teneur'))['teneur__avg']
moyenne_teneurs = round(moyenne_teneur, 2)
moyenne_teneur_etain = refinering.objects.aggregate(Avg('teneur_sortie'))['teneur_sortie__avg']
moyenne_teneur_etains = round(moyenne_teneur_etain, 2)



def nav(request):
    summe_casterie_vendu = sorties.objects.all().filter(produits__id = 1)
    summe_casterie_vendus = summe_casterie_vendu.aggregate(Sum('quantite'))['quantite__sum']

    summe_casterie_achater = entrees.objects.all().filter(produits__id = 1)
    summe_casterie_achaters = summe_casterie_achater.aggregate(Sum('quantite'))['quantite__sum']
    alet1 = 0
    sango = ''
    en_stock = summe_casterie_achaters - summe_casterie_vendus
    if en_stock == 10:
        alet =1
    context = {
        'alet':1,
        'sango':50,
    }


    return render(request, 'pages/header.html',context)

def index(request):
    summe_casterie_vendu = sorties.objects.all().filter(produits__id = 1)
    summe_casterie_vendus = summe_casterie_vendu.aggregate(Sum('quantite'))['quantite__sum']

    summe_casterie_transformer = smelting.objects.all().filter(produits__id = 1)
    summe_casterie_transformers = summe_casterie_transformer.aggregate(Sum('quantite_entrer'))['quantite_entrer__sum']
 
    summe_casterie_achater = entrees.objects.all().filter(produits__id = 1)
    summe_casterie_achaters = summe_casterie_achater.aggregate(Sum('quantite'))['quantite__sum']
    
    en_stocks_casterie = summe_casterie_achaters - (summe_casterie_vendus + summe_casterie_transformers)

    summe_etain_transformer = refinering.objects.all().filter(produits__id = 3)
    summe_etain_transformers = summe_etain_transformer.aggregate(Sum('quantite_sortie'))['quantite_sortie__sum']

    summe_etain_vendu = sorties.objects.all().filter(produits__id = 3)
    summe_etain_vendus = summe_etain_vendu.aggregate(Sum('quantite'))['quantite__sum']
    en_stocks_etain= summe_etain_transformers - (summe_etain_vendus)

    revenu_etain = sorties.objects.all().filter(produits__id = 3)
    revenu_etains = revenu_etain.aggregate(Sum('prix_total'))['prix_total__sum'] 
    sango = 'la quantité en stock de la  casterie est de {} Kg cela ne suffit pas pour effectuer la vente !!'.format(3)

    revenu_casterie = sorties.objects.all().filter(produits__id = 1)
    revenu_casteries = revenu_casterie.aggregate(Sum('prix_total'))['prix_total__sum']
    context = {
        
        'en_stocks':en_stocks_casterie,
        'en_stocks_etain':en_stocks_etain,
        'moyenne_teneur':moyenne_teneurs,
        'moyenne_teneur_etain':moyenne_teneur_etains,
        'revenu_etains':revenu_etains,
        'revenu_casteries':revenu_casteries,
        'alet':1,
        'sango':sango,
        
    }
    


    return render(request, 'pages/index.html',context)
def main(request):
    


    return render(request, 'pages/main.html')
    
def sortie_etain_brut(request, id):
    g = smelting.objects.get(id=id)
    
    context = {
        'g': g,
        'moyenne_teneur': moyenne_teneur,
    }

    return render(request, 'pages/sortie_etain_brut.html',context)

def sortie_etain(request, id):
    g = refinering.objects.get(id=id)
    
    context = {
        'g': g,
        'moyenne_teneur': moyenne_teneur,
    }

    return render(request, 'pages/sortie_etain.html',context)



def updaterecord_bru(request, id):
    
   
    quantite_sorti = request.POST['quantite_out']
    prod_id = request.POST['produit']
    ten_sortie = request.POST['teneur']
    sortierfou = refinering.objects.get(id=id)
    produit_id = produits.objects.get(id = int(prod_id))
    sortierfou.quantite_sortie = quantite_sorti
    sortierfou.produits = produit_id
    sortierfou.teneur_sortie = ten_sortie
    sortierfou.save()
    url = reverse('transformation')
    ret = HttpResponseRedirect(url)
    return ret

def updaterecord(request, id):

    quantite_sorti = request.POST['quantite_out']

    sortierfou = smelting.objects.get(id=id)
    produit_id = produits.objects.get(id = 3)
    sortierfou.quantite_out = quantite_sorti
    sortierfou.produits = produit_id
    sortierfou.save()
    url = reverse('transformation')
    ret = HttpResponseRedirect(url)
    return ret
    


def transformation(request):
    fourrafines = fourrafine.objects.all().values()
    fourcasteries = fourcasterie.objects.all().values()
    smeltings = smelting.objects.select_related('fourcasterie','produits')
    rafinage = refinering.objects.select_related('fourrafine','produits')
    if request.method == 'POST':

        produitt = request.POST['produit']
        fourcasteriess = request.POST['Four']
        produit_id = produits.objects.get(id = int(produitt))
        fourcasterie_id = fourcasterie.objects.get(id = int(fourcasteriess))
        quantite_in = request.POST['quantite']
        entrants = request.POST['entrants']
        
        
        fondre = smelting(produits = produit_id, fourcasterie = fourcasterie_id, quantite_entrer = quantite_in, teneur_entrer = moyenne_teneur, entrants = entrants)
        fondre.save()
        url = reverse('transformation')
        ret = HttpResponseRedirect(url)
        return ret 
    context = {
        
        'moyenne_teneur': moyenne_teneur,
        'smeltings': smeltings,
        'fourcasteries': fourcasteries,
        'produit': produit,
        'fourrafines':fourrafines,
        'rafinage':rafinage,
        
        
    }

    return render(request, 'pages/transformation.html',context)
    
def vente(request):
    sortie = sorties.objects.select_related('clients','produits')
    total_general = sorties.objects.aggregate(Sum('prix_total'))['prix_total__sum']
    total_prix_vente = sorties.objects.aggregate(Sum('prix_vente'))['prix_vente__sum']
    total_quantite = sorties.objects.aggregate(Sum('quantite'))['quantite__sum']
    summe_casterie_vendu = sorties.objects.all().filter(produits__id = 1)
    summe_casterie_vendus = summe_casterie_vendu.aggregate(Sum('quantite'))['quantite__sum']

    summe_casterie_transformer = smelting.objects.all().filter(produits__id = 1)
    summe_casterie_transformers = summe_casterie_transformer.aggregate(Sum('quantite_entrer'))['quantite_entrer__sum']
    

    summe_casterie_achater = entrees.objects.all().filter(produits__id = 1)
    summe_casterie_achaters = summe_casterie_achater.aggregate(Sum('quantite'))['quantite__sum']

    en_stocks = summe_casterie_achaters - (summe_casterie_vendus + summe_casterie_transformers)
    
    if ((summe_casterie_achaters  != None) or ( summe_casterie_vendus != None)) and (summe_casterie_achaters > (summe_casterie_vendus + summe_casterie_transformers)):

        en_stocks = summe_casterie_achaters - (summe_casterie_vendus + summe_casterie_transformers)
        
        
        if request.method == 'POST':
            
            produitt = request.POST['produit']
            clientt = request.POST['client']
            produit_id = produits.objects.get(id = int(produitt))
            client_id = clients.objects.get(id = int(clientt))
            quantite = request.POST['quantite']
            prix_de_vente = request.POST['prix_vente']
            teneur_casterie = moyenne_teneur
            teneur_etain = moyenne_teneur_etain
            
            if en_stocks > 20:
                
                if quantite != '' and prix_de_vente != '':
                    pt = float(quantite) * float(prix_de_vente)
                else:
                    pass
                if int(produitt) == 1 and float(quantite) > en_stocks:
                    if float(quantite) < en_stocks:

                        vente = sorties(clients = client_id, produits = produit_id, prix_vente = prix_de_vente, quantite = quantite, teneur = moyenne_teneur,prix_total = pt)
                        vente.save()
                        url = reverse('vente')
                        ret = HttpResponseRedirect(url)
                        return ret
                    else:
                        pass
                
                else:
                    if float(quantite) < en_stocks:

                        vente = sorties(clients = client_id, produits = produit_id, prix_vente = prix_de_vente, quantite = quantite, teneur =moyenne_teneur_etain ,prix_total = pt)
                        vente.save()
                        url = reverse('vente')
                        ret = HttpResponseRedirect(url)
                    else:
                        pass
            else:
                sangos = 'la quantité en stock de la  casterie est de {} Kg cela ne suffit pas pour effectuer la vente !!'.format(en_stocks)
                alets =1
        else:
            sangos = 'la quantité en stock de la  casterie est de {} Kg cela ne suffit pas pour effectuer la vente !!'.format(en_stocks)
            alets =1
    context = {
        'sortie': sortie,
        'produit': produit,
        'client': client,
        'moyenne_teneur': moyenne_teneur,
        'total_general':total_general,
        'total_prix_vente':total_prix_vente,
        'total_quantite':total_quantite,
        'moyenne_teneur_etain':moyenne_teneur_etain,
        'summe_casterie_vendus':summe_casterie_vendus,
        'summe_casterie_achaters':summe_casterie_achaters,
        'en_stocks':en_stocks,
        # 'sango':sangos,
        # 'alet':alets,

        
    }
 
    return render(request, 'pages/vente.html',context)

def achat(request):
    entres = entrees.objects.select_related('fournisseurs','produits')
    total_general = entrees.objects.aggregate(Sum('prix_total'))['prix_total__sum']
    total_prix_vente = entrees.objects.aggregate(Sum('prix_achat'))['prix_achat__sum']
    total_quantite = entrees.objects.aggregate(Sum('quantite'))['quantite__sum']
    summe_casterie_vendu = entrees.objects.all().filter(produits__id = 1)
    summe_casterie_vendus = summe_casterie_vendu.aggregate(Sum('quantite'))['quantite__sum']

    summe_casterie_achater = entrees.objects.all().filter(produits__id = 1)
    summe_casterie_achaters = summe_casterie_achater.aggregate(Sum('quantite'))['quantite__sum']

    
        
        
    if request.method == 'POST':
        
        produitt = request.POST['produit']
        fourcasteriess = request.POST['client']
        produit_id = produits.objects.get(id = int(produitt))
        fourcasteriess_id = fournisseurs.objects.get(id = int(fourcasteriess))
        quantite = request.POST['quantite']
        prix_achatq = request.POST['prix_achat']
        tagss = request.POST['tag']
        teneur = request.POST['teneur']
        teneur_casterie = moyenne_teneur
        teneur_etain = moyenne_teneur_etain
        
        
            
        if quantite != '' and prix_achatq != '':
            pt = float(quantite) * float(prix_achatq)
        else:
            pass

            

        achatss = entrees( fournisseurs = fourcasteriess_id, produits = produit_id, prix_achat = prix_achatq , quantite = quantite, teneur = teneur ,numero_tag = tagss ,prix_total = pt)
        achatss.save()
        url = reverse('achat')
        ret = HttpResponseRedirect(url)
        return ret
           
            
       
      
    context = {
        
        'produit': produit,
        'fournisseur': fournisseur,
        'moyenne_teneur': moyenne_teneur,
        'total_general':total_general,
        'total_prix_vente':total_prix_vente,
        'total_quantite':total_quantite,
        'moyenne_teneur_etain':moyenne_teneur_etain,
        'summe_casterie_vendus':summe_casterie_vendus,
        'summe_casterie_achaters':summe_casterie_achaters,
        
        'entres':entres,
        
    }
    return render(request, 'pages/achat.html',context)

