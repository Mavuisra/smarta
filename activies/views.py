from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from .models import clients, entrees,sorties, produits, clients, smelting, fourcasterie, refinering, fourrafine,stock
from django.db.models import Sum, Avg, Count
# Create your views here.

produit = produits.objects.all().values()
client = clients.objects.all().values()

moyenne_teneur = entrees.objects.aggregate(Avg('teneur'))['teneur__avg']
moyenne_teneur_etain = refinering.objects.aggregate(Avg('teneur_sortie'))['teneur_sortie__avg']


def nav(request):
    summe_casterie_vendu = sorties.objects.all().filter(produits__id = 1)
    summe_casterie_vendus = summe_casterie_vendu.aggregate(Sum('quantite'))['quantite__sum']

    summe_casterie_achater = entrees.objects.all().filter(produits__id = 1)
    summe_casterie_achaters = summe_casterie_achater.aggregate(Sum('quantite'))['quantite__sum']
    alet1 = 0
    sango = ''
    en_stock = summe_casterie_achaters - summe_casterie_vendus
    if en_stock == 10:
        sango = 'la quantité en stock de la  casterie est de {} Kg cela ne suffit pas pour effectuer la vente !!'.format(en_stock)
        alet =1
    context = {
        'alet':alet1,
        'sango':sango,
    }


    return render(request, 'pages/header.html',context)

def index(request):
    


    return render(request, 'pages/index.html')
    
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

    summe_casterie_achater = entrees.objects.all().filter(produits__id = 1)
    summe_casterie_achaters = summe_casterie_achater.aggregate(Sum('quantite'))['quantite__sum']

    en_stocks = summe_casterie_achaters - summe_casterie_vendus
    
    if ((summe_casterie_achaters  != None) or ( summe_casterie_vendus != None)) and (summe_casterie_achaters > summe_casterie_vendus):

        en_stocks = summe_casterie_achaters - summe_casterie_vendus
        
        
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
                if int(produitt) == 1:
                    vente = sorties(clients = client_id, produits = produit_id, prix_vente = prix_de_vente, quantite = quantite, teneur = moyenne_teneur,prix_total = pt)
                    vente.save()
                    url = reverse('vente')
                    ret = HttpResponseRedirect(url)
                    return ret
                
                else:
                    
                    vente = sorties(clients = client_id, produits = produit_id, prix_vente = prix_de_vente, quantite = quantite, teneur =moyenne_teneur_etain ,prix_total = pt)
                    vente.save()
                    url = reverse('vente')
                    ret = HttpResponseRedirect(url)
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
    context = {
        
        'entres':entres,
        
    }
    return render(request, 'pages/achat.html',context)

