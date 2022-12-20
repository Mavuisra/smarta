from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import clients, entrees,sorties, produits, clients, smelting, fourcasterie, refinering, fourrafine,fournisseurs,users
from django.db.models import Sum, Avg, Count
from django.db.models.functions import TruncMonth
from django.contrib.auth.forms import UserCreationForm
from .form import CreationUserForm,usersForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorator import unauthenticated_user,allowed_users


# Create your views here.

produit = produits.objects.all().values()
client = clients.objects.all().values()
fournisseur = fournisseurs.objects.all().values()

def user_profil(request):
    user = request.user.users
    form = usersForm(instance=user)
    if request.method == 'POST':
        form = usersForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
    context = {
           'form':form,
    }

    
    return render(request, 'pages/user_profil.html',context)
@unauthenticated_user
def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'information invalides')
    context = {
        
    
    }
    return render(request, 'pages/login.html',context)

def createUser(request):

    form = CreationUserForm()
    if request.method == 'POST':
        form = CreationUserForm(request.POST)
        if form.is_valid:
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name = 'user')
            user.groups.add(group)
            users.objects.create(
                user = user,
                name = users.name

            )

            messages.success(request, f"l'utilisateur {username} a ete crée avec succès")
            return redirect('login')
        else:
            pass

    context = {
    'form':form, 
    
    }
    return render(request, 'pages/CreateUser.html',context)

def logoutpage(request):
    logout(request)
    return redirect('login')

def facture(request, id):
    gg = sorties.objects.get(id=id)

    context = {
        'g': gg,
    
    }

    return render(request, 'pages/facture.html',context)

def clientst(request):
    if request.method  == 'POST':
        nomClient = request.POST['name']
        villeClient = request.POST['Telephone']
        sexeClient = request.POST['Sexe']
        saveClient = clients(nom_clients = nomClient, sexe = sexeClient, telephone = villeClient)
        saveClient.save()
        url = reverse('vente')
        ret = HttpResponseRedirect(url)
        return ret
    else:
        print('null')
    return render(request, 'pages/client.html')
    
def fournisseurss(request):
    if request.method  == 'POST':
        fou = request.POST['name']
        tel = request.POST['Telephone']
        sexe = request.POST['Sexe']
        sf = fournisseurs(nom_fournisseurs = fou, sexe = sexe, telephone =tel )
        sf.save()
        url = reverse('achat')
        ret = HttpResponseRedirect(url)
        return ret
    else:
        print('null')
    return render(request, 'pages/fournisseur.html')

@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['admin'])
def index(request):

    moyenne_teneur_etain = refinering.objects.aggregate(Avg('teneur_sortie'))['teneur_sortie__avg']
    moyenne_teneur_etains = round(moyenne_teneur_etain, 2)
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
    

    revenu_casterie = sorties.objects.all().filter(produits__id = 1)
    revenu_casteries = revenu_casterie.aggregate(Sum('prix_total'))['prix_total__sum']
    # rapport = sorties.objects.filter().extra({'month':"Extract(month FROM 	sorties.date_sortie )"} ).values_list('month').annotate(Sum('prix_total'))
    moyenne_teneur = entrees.objects.aggregate(Avg('teneur'))['teneur__avg']
    moyenne_teneurs = round(moyenne_teneur, 2)
    # g = sorties.objects.annotate(month = TruncMonth('date_sortie')).values('month').annotate(rev = Sum('prix_total')).values('rev','month')
    g = sorties.objects.values('date_sortie__month').annotate(tota = Sum('prix_total')).values('date_sortie__month','tota')
    print('hello',g)
     
    context = {
        'en_stocks':en_stocks_casterie,
        'en_stocks_etain':en_stocks_etain,
        'moyenne_teneurs':moyenne_teneurs,
        'moyenne_teneur_etains':moyenne_teneur_etains,
        'revenu_etains':revenu_etains,
        'revenu_casteries':revenu_casteries,
        
        
    }
    


    return render(request, 'pages/index.html',context)
@login_required(login_url = 'login')
def rafinage(request):
    moyenne_teneur_etain = refinering.objects.aggregate(Avg('teneur_sortie'))['teneur_sortie__avg']
    moyenne_teneur_etains = round(moyenne_teneur_etain, 2)
    fourrafines = fourrafine.objects.all().values()
    fourcasteries = fourcasterie.objects.all().values()
    smeltings = smelting.objects.select_related('fourcasterie','produits')
    rafinage = refinering.objects.select_related('fourrafine','produits')
    
    summe_casterie_sortie_four = smelting.objects.all().filter(produits__id = 1)
    summe_casterie_sortie_fours = summe_casterie_sortie_four.aggregate(Sum('quantite_out'))['quantite_out__sum']
   
    etain_entrain = refinering.objects.all().filter(produits__id = 3)
    etain_entrains = etain_entrain.aggregate(Sum('quantite_entree'))['quantite_entree__sum']
    etain_sortie = etain_entrain.aggregate(Sum('quantite_sortie'))['quantite_sortie__sum']
    en_four = summe_casterie_sortie_fours - etain_entrains

    if summe_casterie_sortie_fours > etain_entrains:
        en_four = summe_casterie_sortie_fours - etain_entrains
        if request.method == 'POST':
            produitt = request.POST['produit']
            fourcasteriess = request.POST['Four']
            produit_id = produits.objects.get(id = int(produitt))
            fourcasterie_id = fourrafine.objects.get(id = int(fourcasteriess))
            quantite_in = request.POST['quantite']
            entrants = request.POST['entrants']
            if en_four > float(quantite_in):

                fondre = refinering(produits = produit_id, fourrafine = fourcasterie_id, quantite_entree = quantite_in, teneur_sortie = moyenne_teneur_etains, entrants = entrants)
                fondre.save()
                url = reverse('rafinage')
                ret = HttpResponseRedirect(url)
                return ret 
    context = {
        
        'moyenne_teneur': moyenne_teneur_etains,
        'smeltings': smeltings,
        'fourcasteries': fourcasteries,
        'produit': produit,
        'fourrafines':fourrafines,
        'rafinage':rafinage,
        'moyenne_teneur_etains':moyenne_teneur_etains,
        'etain_sortie': en_four,
        'en_four':en_four,
        'summe_casterie_sortie_fours':summe_casterie_sortie_fours,
        'etain_entrains':etain_entrains,
        'etain_sortie':etain_sortie,
        
        
    }

    return render(request, 'pages/rafinage.html',context)

@login_required(login_url = 'login')
def sortie_etain_brut(request, id):
    gg = smelting.objects.get(id=id)
    moyenne_teneur = entrees.objects.aggregate(Avg('teneur'))['teneur__avg']
    moyenne_teneurs = round(moyenne_teneur, 2)
    context = {
        'g': gg,
        'moyenne_teneur': moyenne_teneurs,
    }

    return render(request, 'pages/sortie_etain_brut.html',context)
@login_required(login_url = 'login')
def sortie_etain(request, id):
    moyenne_teneur = entrees.objects.aggregate(Avg('teneur'))['teneur__avg']
    moyenne_teneurs = round(moyenne_teneur, 2)
    g = refinering.objects.get(id=id)
    
    context = {
        'g': g,
        'moyenne_teneur': moyenne_teneurs,
        'produit':produit,
    }

    return render(request, 'pages/sortie_etain.html',context)
@login_required(login_url = 'login')
def updaterecord_bru(request, id):
    
    quantite_entre = request.POST['quantite_entree']

    quantite_sorti = request.POST['quantite_out']
    produit_id = produits.objects.get(id = 3)
    ten_sortie = request.POST['teneur']
    sortierfou = refinering.objects.get(id=id)
    
    if float(quantite_sorti) <=  float(quantite_entre):
        sortierfou.quantite_entree = float(sortierfou.quantite_entree) - float(quantite_sorti)
        sortierfou.produits = produit_id
        sortierfou.teneur_sortie = ten_sortie
        sortierfou.quantite_sortie += float(quantite_sorti)
        sortierfou.save()

        url = reverse('rafinage')
        ret = HttpResponseRedirect(url)
        return ret
    else:
        url = reverse('rafinage')
        ret = HttpResponseRedirect(url)
        return ret
@login_required(login_url = 'login')
def updaterecord(request, id):

    quantite_sorti = request.POST['quantite_out']
    quantite_entre = request.POST['quantite']
    sortierfou = smelting.objects.get(id=id)
    produit_id = produits.objects.get(id = 4)
    
    if float(quantite_sorti) <=  float(quantite_entre):
        sortierfou.quantite_entrer = float(sortierfou.quantite_entrer) - float(quantite_sorti)
        sortierfou.produits = produit_id
        sortierfou.quantite_out += float(quantite_sorti)
        sortierfou.save()
        url = reverse('transformation')
        ret = HttpResponseRedirect(url)
        return ret
    else:
        url = reverse('transformation')
        ret = HttpResponseRedirect(url)
        return ret
@login_required(login_url = 'login')
def transformation(request):
    moyenne_teneur_etain = refinering.objects.aggregate(Avg('teneur_sortie'))['teneur_sortie__avg']
    moyenne_teneur_etains = round(moyenne_teneur_etain, 2)
    fourrafines = fourrafine.objects.all().values()
    fourcasteries = fourcasterie.objects.all().values()
    smeltings = smelting.objects.select_related('fourcasterie','produits')
    rafinage = refinering.objects.select_related('fourrafine','produits')
    moyenne_teneur = entrees.objects.aggregate(Avg('teneur'))['teneur__avg']
    moyenne_teneurs = round(moyenne_teneur, 2)
    summe_casterie_four = smelting.objects.all().filter(produits__id = 1)
    summe_casterie_fours = summe_casterie_four.aggregate(Sum('quantite_entrer'))['quantite_entrer__sum']
    summe_etain_brut_fours = summe_casterie_four.aggregate(Sum('quantite_out'))['quantite_out__sum']

    summe_casterie_achater = entrees.objects.all().filter(produits__id = 1)
    summe_casterie_achaters = summe_casterie_achater.aggregate(Sum('quantite'))['quantite__sum']
    
    summe_casterie_vendu = sorties.objects.all().filter(produits__id = 1)
    summe_casterie_vendus = summe_casterie_vendu.aggregate(Sum('quantite'))['quantite__sum']
    en_four = summe_casterie_achaters - summe_casterie_fours
    if ((summe_casterie_achaters  != None) or ( summe_casterie_vendus != None)) and (summe_casterie_achaters > (summe_casterie_vendus + summe_casterie_fours)):

        en_four = summe_casterie_achaters - (summe_casterie_vendus + summe_casterie_fours)
        if request.method == 'POST':
            
            produitt = request.POST['produit']
            fourcasteriess = request.POST['Four']
            produit_id = produits.objects.get(id = int(produitt))
            fourcasterie_id = fourcasterie.objects.get(id = int(fourcasteriess))
            quantite_in = request.POST['quantite']
            entrants = request.POST['entrants']
            if en_four > float(quantite_in):

                fondre = smelting(produits = produit_id, fourcasterie = fourcasterie_id, quantite_entrer = quantite_in, teneur_entrer = moyenne_teneurs, entrants = entrants)
                fondre.save()
                url = reverse('transformation')
                ret = HttpResponseRedirect(url)
                return ret 
    context = {
        
        'moyenne_teneur': moyenne_teneurs,
        'smeltings': smeltings,
        'fourcasteries': fourcasteries,
        'produit': produit,
        'fourrafines':fourrafines,
        'rafinage':rafinage,
        'moyenne_teneur_etains':moyenne_teneur_etains,
        'en_four': en_four,
        'summe_casterie_fours':summe_casterie_fours,
        'summe_etain_brut_fours':summe_etain_brut_fours,
        
    }

    return render(request, 'pages/transformation.html',context)
@login_required(login_url = 'login')
def vente(request):
    moyenne_teneur = entrees.objects.aggregate(Avg('teneur'))['teneur__avg']
    moyenne_teneurs = round(moyenne_teneur, 2)
    summe_casterie_vendu = sorties.objects.all().filter(produits__id = 1)
    summe_casterie_vendus = summe_casterie_vendu.aggregate(Sum('quantite'))['quantite__sum']
    total_prix_vente = summe_casterie_vendu.aggregate(Sum('prix_vente'))['prix_vente__sum']
    prix_total = summe_casterie_vendu.aggregate(Sum('prix_total'))['prix_total__sum']

    summe_casterie_transformer = smelting.objects.all().filter(produits__id = 1)
    summe_casterie_transformers = summe_casterie_transformer.aggregate(Sum('quantite_entrer'))['quantite_entrer__sum']
    

    summe_casterie_achater = entrees.objects.all().filter(produits__id = 1)
    summe_casterie_achaters = summe_casterie_achater.aggregate(Sum('quantite'))['quantite__sum']

    en_stocks = None
    sangos= None
    alert = 0
    
    
    if (((summe_casterie_achaters  != None) or ( summe_casterie_vendus != None))) and (summe_casterie_achaters > (summe_casterie_vendus + summe_casterie_transformers)):

        en_stocks = summe_casterie_achaters - (summe_casterie_vendus + summe_casterie_transformers)
        
        
        if request.method == 'POST':
            
            produitt = request.POST['produit']
            clientt = request.POST['client']
            produit_id = produits.objects.get(id = int(produitt))
            client_id = clients.objects.get(id = int(clientt))
            quantite = request.POST['quantite']
            prix_de_vente = request.POST['prix_vente']
        
            
            if en_stocks > 20:
                
                if quantite != '' and prix_de_vente != '':
                    
                
                    if float(quantite) < en_stocks:
                        pt = float(quantite) * float(prix_de_vente)
                        vente = sorties(clients = client_id, produits = produit_id, prix_vente = prix_de_vente, quantite = quantite, teneur = moyenne_teneurs,prix_total = pt)
                        vente.save()
                        url = reverse('vente')
                        ret = HttpResponseRedirect(url)
                        return ret
                        
                
                    else:
                        sangos = 'la quantité en stock de la  casterie est de {} Kg mais vous voulez vendre {} kg cette operation est impossible!!'.format(en_stocks,quantite)
                        alert = alert+1
                else:
                        sangos = 'remplissez touts les champs'
                        
            else:
                sangos = 'la quantité en stock de la  casterie est de {} Kg cela ne suffit pas pour effectuer la vente !!'.format(en_stocks)
                alert = alert+1
    context = {
        'sortie': summe_casterie_vendu,
        'produit': produit,
        'client': client,
        'moyenne_teneur':round(entrees.objects.aggregate(Avg('teneur'))['teneur__avg'],2),
        'total_general':summe_casterie_vendus,
        'total_prix_vente':total_prix_vente,
        'prix_total':prix_total,
        'summe_casterie_achaters':summe_casterie_achaters,
        'en_stocks':en_stocks,
        'sango':sangos,
        'summe_casterie_transformers':summe_casterie_transformers,
        'summe_casterie_vendus':summe_casterie_vendus,
        'alert':alert,

        
    }
 
    return render(request, 'pages/vente.html',context)
@login_required(login_url = 'login')
def achat(request):

   
    entres = entrees.objects.select_related('fournisseurs','produits')
    total_general = entrees.objects.aggregate(Sum('prix_total'))['prix_total__sum']
    total_prix_vente = entrees.objects.aggregate(Sum('prix_achat'))['prix_achat__sum']
    total_quantite = entrees.objects.aggregate(Sum('quantite'))['quantite__sum']
    summe_casterie_vendu = entrees.objects.all().filter(produits__id = 1)
    summe_casterie_vendus = summe_casterie_vendu.aggregate(Sum('quantite'))['quantite__sum']

    summe_casterie_achater = entrees.objects.all().filter(produits__id = 1)
    summe_casterie_achaters = summe_casterie_achater.aggregate(Sum('quantite'))['quantite__sum']
    
    summe_casterie_four = smelting.objects.all().filter(produits__id = 1)
    summe_casterie_fours = summe_casterie_four.aggregate(Sum('quantite_entrer'))['quantite_entrer__sum']

    summe_casterie_vendu = sorties.objects.all().filter(produits__id = 1)
    summe_casterie_vendus = summe_casterie_vendu.aggregate(Sum('quantite'))['quantite__sum']
    moyenne_teneur = entrees.objects.aggregate(Avg('teneur'))['teneur__avg']
    moyenne_teneurs = round(moyenne_teneur, 2)
    en_four = summe_casterie_achaters - (summe_casterie_vendus + summe_casterie_fours)

    
        
        
    if request.method == 'POST':
        
        produitt = request.POST['produit']
        fourcasteriess = request.POST['client']
        produit_id = produits.objects.get(id = int(produitt))
        fourcasteriess_id = fournisseurs.objects.get(id = int(fourcasteriess))
        quantite = request.POST['quantite']
        prix_achatq = request.POST['prix_achat']
        tagss = request.POST['tag']
        teneur = request.POST['teneur']
       
        
            
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
        'total_general':total_general,
        'total_prix_vente':total_prix_vente,
        'total_quantite':total_quantite,
        'summe_casterie_vendus':summe_casterie_vendus,
        'summe_casterie_achaters':summe_casterie_achaters,
        'en_four':en_four,
        'entres':entres,
        'moyenne_teneurs':moyenne_teneurs,
        'summe_casterie_fours':summe_casterie_fours,
        
        
    }
    return render(request, 'pages/achat.html',context)
@login_required(login_url = 'login')
def vente_etain(request):
    
    summe_casterie_vendu = sorties.objects.all().filter(produits__id = 3)
    summe_casterie_vendus = summe_casterie_vendu.aggregate(Sum('quantite'))['quantite__sum']
    total_prix_vente = summe_casterie_vendu.aggregate(Sum('prix_vente'))['prix_vente__sum']
    prix_total = summe_casterie_vendu.aggregate(Sum('prix_total'))['prix_total__sum']
    df = request.user
    print(prix_total)


    en_stocks = None
    sangos= None
    alert = 0
    summe_etain_transformer = refinering.objects.all().filter(produits__id = 3)
    summe_etain_transformers = summe_etain_transformer.aggregate(Sum('quantite_sortie'))['quantite_sortie__sum']

    summe_etain_vendu = sorties.objects.all().filter(produits__id = 3)
    summe_etain_vendus = summe_etain_vendu.aggregate(Sum('quantite'))['quantite__sum']
    en_stocks_etain= summe_etain_transformers - summe_etain_vendus

    
    
    if summe_etain_transformers > summe_etain_vendus:

        en_stocks_etain = summe_etain_transformers - summe_etain_vendus
        
        
        if request.method == 'POST':
            
            produitt = request.POST['produit']
            clientt = request.POST['client']
            produit_id = produits.objects.get(id = int(produitt))
            client_id = clients.objects.get(id = int(clientt))
            user = request.POST['user']
            user_id = users.objects.get(id = int(user))

            quantite = request.POST['quantite']
            prix_de_vente = request.POST['prix_vente']
            
            
            if en_stocks_etain > 10:
                
                if quantite != None and prix_de_vente != None:
                    
                    if float(quantite) < en_stocks_etain:
                        pt = float(quantite) * float(prix_de_vente)
                        vente = sorties(user = user_id, clients = client_id, produits = produit_id, prix_vente = prix_de_vente, quantite = quantite, teneur = round(refinering.objects.aggregate(Avg('teneur_sortie'))['teneur_sortie__avg'],2),prix_total = pt)
                        vente.save()
                        url = reverse('vente_etain')
                        ret = HttpResponseRedirect(url)
                        return ret
                        
                
                    else:
                        sangos = 'la quantité en stock de l\'etain est de {} Kg cela ne suffit pas pour effectuer une vente !!'.format(en_stocks_etain)
                        alert = alert+1
                else:
                        sangos = 'remplissez touts les champs'
                        alets =1
            else:
                sangos = 'la quantité en stock de la  casterie est de {} Kg cela ne suffit pas pour effectuer la vente !!'.format(en_stocks_etain)
                alets =1
    context = {
        'sortie': summe_casterie_vendu,
        'produit': produit,
        'client': client,
        'moyenne_teneur':round(refinering.objects.aggregate(Avg('teneur_sortie'))['teneur_sortie__avg'],2),
        'total_general':summe_casterie_vendus,
        'total_prix_vente':total_prix_vente,
        'prix_total':prix_total,
        'en_stocks':en_stocks_etain,
        'sango':sangos,
        'summe_casterie_vendus':summe_casterie_vendus,
        'summe_etain_vendus':summe_etain_vendus,
        'summe_etain_transformers':summe_etain_transformers,
        'df':df,
     
        
    }
 
    return render(request, 'pages/vente_etain.html', context)
