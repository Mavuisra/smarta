import codecs
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import *
from django.db.models import Sum, Avg, Count
from django.db.models.functions import TruncMonth, TruncYear, TruncWeek, TruncDay
from django.contrib.auth.forms import UserCreationForm
from .form import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorator import unauthenticated_user, allowed_users
import numpy as np
from.fonctions import myClasses
import datetime

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
        'form': form,
    }

    return render(request, 'pages/user_profil.html', context)
@unauthenticated_user
def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'information invalides')
    context = {


    }
    return render(request, 'pages/login.html', context)

def createUser(request):

    form = CreationUserForm()
    if request.method == 'POST':
        form = CreationUserForm(request.POST)
        if form.is_valid:
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='user')
            user.groups.add(group)
            users.objects.create(
                user=user,
                name=users.name

            )

            messages.success(
                request, f"l'utilisateur {username} a ete crée avec succès")
            return redirect('login')
        else:
            pass

    context = {
        'form': form,

    }
    return render(request, 'pages/CreateUser.html', context)

def logoutpage(request):
    logout(request)
    return redirect('login')
@login_required(login_url='login')
def facture(request, id):
    gg = sorties.objects.get(id=id)

    context = {
        'g': gg,

    }

    return render(request, 'pages/facture.html', context)


@allowed_users(allowed_roles=['admin'])
def index(request):
    stock_c = myClasses()
    moyenne_teneur = stock_c.moyenne_teneur()
    moyenne_teneur_etain = stock_c.moyenne_teneur_etain()
    stock_casterie = stock_c.stock_casterie()
    stasts = stock_c.stats_all()
    somme_vente = stasts.get("somme_vente")
    somme_achat = stasts.get("somme_achat")
    somme_trans_cast = stasts.get("somme_trans_cast")
    somme_livree_cast =stasts.get("somme_livree_cast") 
    s_qt_non_livree = stasts.get("s_qt_non_livree")



    context = {
        'moyenne_teneur_etain':moyenne_teneur_etain,
        's_qt_non_livree':s_qt_non_livree,
        'somme_livree_cast':somme_livree_cast,
        'somme_trans_cast':somme_trans_cast,
        'somme_achat':somme_achat,
        'somme_vente':somme_vente,
        'stock_casterie':stock_casterie,
        'moyenne_teneur':round(moyenne_teneur),
        
    }
    return render(request, 'pages/index.html', context)

def Achat(request):
    stock_c = myClasses()
    stock_casterie = stock_c.stock_casterie()
    

    
    all_sortie = sorties.objects.all().values()
    all_smelting = transformations.objects.all().values()
    all_achats = entrees.objects.all().values()
    all_acha = entrees.objects.all()
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
    print(moyenne_teneur,stock_casterie)
    
    
    


    stasts = stock_c.stats_all()
    somme_vente = stasts.get("somme_vente")
    somme_achat = stasts.get("somme_achat")
    somme_trans_cast = stasts.get("somme_trans_cast")
    somme_livree_cast =stasts.get("somme_livree_cast") 
    s_qt_non_livree = stasts.get("s_qt_non_livree")



    context = {
        's_qt_non_livree':s_qt_non_livree,
        'somme_livree_cast':somme_livree_cast,
        'somme_trans_cast':somme_trans_cast,
        'somme_achat':somme_achat,
        'somme_vente':somme_vente,
        'stock_casterie':stock_casterie,
        'moyenne_teneur':round(moyenne_teneur),
        'all_achats':all_acha,
        'all_quantite': all_achats.aggregate(Sum('quantite_en_kg'))['quantite_en_kg__sum'],
        'all_prices': all_achats.aggregate(Sum('prix_achat_en_dollard'))['prix_achat_en_dollard__sum'],
        'all_amount': all_achats.aggregate(Sum('montant_depanses_en_dollard'))['montant_depanses_en_dollard__sum'],
        'all_total_prices': all_achats.aggregate(Sum('prix_total_en_dollard'))['prix_total_en_dollard__sum'],
    }
    return render(request, 'pages/achat.html', context)

def add_Achat(request):
    stock_c = myClasses()
    stock_casterie = stock_c.stock_casterie()
    form = AchatForm()
    all_achats = entrees.objects.all()

    if request.method == 'POST':
        form = AchatForm(request.POST)
        quantite = request.POST.get("quantite_en_kg")  
        if quantite > stock_casterie:

            if form.is_valid:
                form.save()
                return redirect('achat')
        else:
            messages.error("la quantité en stock est insuffisante")
            

    context = {
        'all_achats':all_achats,
        'form':form,
    }
    return render(request, 'pages/ajout_achat.html', context)

def update_achat(request, id):
    
    all_achats = entrees.objects.get(id = id)
    form = AchatForm(instance=all_achats)
    if request.method == 'POST':
        form = AchatForm(request.POST, instance=all_achats)
        if form.is_valid:
            form.save()
            return redirect('achat')
        

    context = {
        'all_achats':all_achats,
        'form':form,
    }
    return render(request, 'pages/ajout_achat.html', context)
    
def fondrerie(request):
    stock_c = myClasses()
    all_fondrerie = transformations.objects.all()
    stasts = stock_c.stats_all()
    somme_vente = stasts.get("somme_vente")
    somme_achat = stasts.get("somme_achat")
    somme_trans_cast = stasts.get("somme_trans_cast")
    somme_livree_cast =stasts.get("somme_livree_cast") 
    s_qt_non_livree = stasts.get("s_qt_non_livree")
    stock_casterie = stock_c.stock_casterie()
    moyenne_teneur = stock_c.moyenne_teneur()

    context = {
        's_qt_non_livree':s_qt_non_livree,
        'somme_livree_cast':somme_livree_cast,
        'somme_trans_cast':somme_trans_cast,
        'somme_achat':somme_achat,
        'somme_vente':somme_vente,
        'stock_casterie':stock_casterie,
        'moyenne_teneur':round(moyenne_teneur),
        'all_fondrerie':all_fondrerie,
    }
    return render(request, 'pages/fondrerie.html', context)

def add_fondre(request):
    all_fondrerie = transformations.objects.all()
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
    print(moyenne_teneur)
    form = FondrerieForm()
    if request.method == 'POST':
        form = FondrerieForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('fondrerie')
        

    context = {
        'moyenne_teneur':moyenne_teneur,
        'form':form,
    }
    return render(request, 'pages/ajouter_four.html', context)

def update_fondre(request, id):
    all_fondrerie = transformations.objects.get(id = id)
    form = FondrerieForm(instance=all_fondrerie)
    if request.method == 'POST':
        form = FondrerieForm(request.POST, instance=all_fondrerie)
        if form.is_valid:
            form.save()
            return redirect('fondrerie')
        

    context = {
        
        'form':form,
    }
    return render(request, 'pages/ajouter_four.html', context)

def rafinage(request):
    stock_c = myClasses()
    all_fondrerie = transformations.objects.all()
    stasts = stock_c.stats_all()
    stock_etain = stock_c.stock_etain()
    teneur_etain = stock_c.moyenne_teneur_etain()
    s_qt_entrer_etain = stasts.get("s_qt_entrer_etain")
    s_qt_transformer_etain = stasts.get("s_qt_transformer_etain")
    context = {
        'teneur_etain':teneur_etain,
        'stock_etain':stock_etain,
        's_qt_entrer_etain':s_qt_entrer_etain,
        's_qt_transformer_etain':s_qt_transformer_etain,
        'all_fondrerie':all_fondrerie,
    }
    return render(request, 'pages/rafinages.html', context)

def update_rafinage(request, id):
    all_fondrerie = transformations.objects.get(id = id)
    form = RafinageForm(instance=all_fondrerie)
    if request.method == 'POST':
        form = RafinageForm(request.POST, instance=all_fondrerie)
        if form.is_valid:
            form.save()
            return redirect('rafinage')
        

    context = {
        'all_fondrerie':all_fondrerie,
        
        'form':form,
    }
    return render(request, 'pages/ajouter_four.html', context)

def vente(request):
    stock_c = myClasses()
    moyenne_teneur = stock_c.moyenne_teneur()
    stock_casterie = stock_c.stock_casterie()
    all_ventes = sorties.objects.all().filter(produits_id  = 5)
    stasts = stock_c.stats_all()
    somme_vente = stasts.get("somme_vente")
    somme_achat = stasts.get("somme_achat")
    somme_trans_cast = stasts.get("somme_trans_cast")
    somme_livree_cast =stasts.get("somme_livree_cast") 
    s_qt_non_livree = stasts.get("s_qt_non_livree")



    context = {
        'moyenne_teneur':round(moyenne_teneur),
        's_qt_non_livree':s_qt_non_livree,
        'somme_livree_cast':somme_livree_cast,
        'somme_trans_cast':somme_trans_cast,
        'somme_achat':somme_achat,
        'somme_vente':somme_vente,
        'stock_casterie':stock_casterie,
        'all_quantite': all_ventes.aggregate(Sum('quantite_en_kg'))['quantite_en_kg__sum'],
        'all_prices': all_ventes.aggregate(Sum('prix_vente_en_dollard'))['prix_vente_en_dollard__sum'],
        'all_total_prices': all_ventes.aggregate(Sum('prix_total_en_dollard'))['prix_total_en_dollard__sum'],
        'all_ventes':all_ventes,
    }
    return render(request, 'pages/vente.html', context)

def add_vente(request):
    teneur= myClasses()
    stock_c = myClasses()
    stock_casterie_etain = stock_c.stock_casterie()
    moyenne_teneur = teneur.moyenne_teneur()
    form = VenteForm()
    all_ventes = sorties.objects.all().values()
    
    if request.method == 'POST':
        quantite = request.POST.get("quantite_en_kg")
        form = VenteForm(request.POST)
        if float(quantite) < stock_casterie_etain:
            if form.is_valid:
                form.save()
                return redirect('vente')
        else:
             messages.info(request, 'quantite en stock est insuffisante')

        

    context = {
        'moyenne_teneur':round(moyenne_teneur,2),
        'all_achats':all_ventes,
        'form':form,
    }
    return render(request, 'pages/ajout_vente.html', context)

def update_vente(request, id):
    teneur= myClasses()
    moyenne_teneur = teneur.moyenne_teneur()
    all_ventes = sorties.objects.get(id = id)
    form = VenteForm(instance=all_ventes)
    if request.method == 'POST':
        form = VenteForm(request.POST, instance=all_ventes)
        if form.is_valid:
            form.save()
            return redirect('vente')
        

    context = {
        'moyenne_teneur':round(moyenne_teneur,2),
        'all_achats':all_ventes,
        'form':form,
    }
    return render(request, 'pages/ajout_vente.html', context)


def vente_etain(request):
    stock_c = myClasses()
    
    stock_etain = stock_c.stock_etain()
    stasts = stock_c.stats_all()
    s_qt_non_livree_etain = stasts.get("s_qt_non_livree_etain")
    s_qt_livree_etain = stasts.get("s_qt_livree_etain")
    s_qt_vente_vente = stasts.get("s_qt_vente_vente")
    s_qt_transformer_etain = stasts.get("s_qt_transformer_etain")
    all_ventes = sorties.objects.all().filter(produits_id = 6)
    s_qt_non_livree = stasts.get("s_qt_non_livree")



    context = {
        'stock_etain':stock_etain,
        's_qt_non_livree':s_qt_non_livree,
        's_qt_non_livree_etain':s_qt_non_livree_etain,
        's_qt_livree_etain':s_qt_livree_etain,
        's_qt_vente_vente':s_qt_vente_vente,
        's_qt_transformer_etain':s_qt_transformer_etain,
        'all_quantite': all_ventes.aggregate(Sum('quantite_en_kg'))['quantite_en_kg__sum'],
        'all_prices': all_ventes.aggregate(Sum('prix_vente_en_dollard'))['prix_vente_en_dollard__sum'],
        'all_total_prices': all_ventes.aggregate(Sum('prix_total_en_dollard'))['prix_total_en_dollard__sum'],
        'all_ventes':all_ventes,
    }
    return render(request, 'pages/vente_etain.html', context) 
def add_vente_etain(request):
    teneur= myClasses()
    stock_c = myClasses()
    stock_casterie = stock_c.stock_casterie()
    moyenne_teneur = teneur.moyenne_teneur_etain()
    form = VenteForm()
    all_ventes = sorties.objects.all().values().filter(produits_id = 6)
    
    if request.method == 'POST':
        quantite = request.POST.get("quantite_en_kg")
        form = VenteForm(request.POST)
        if float(quantite) < stock_casterie:
            if form.is_valid:
                form.save()
                return redirect('vente_etain')
        else:
             messages.info(request, 'quantite en stock est insuffisante')

        

    context = {
        'moyenne_teneur':round(moyenne_teneur,2),
        'all_achats':all_ventes,
        'form':form,
    }
    return render(request, 'pages/ajout_vente_etain.html', context)

def update_vente_etain(request, id):
    teneur= myClasses()
    moyenne_teneur = teneur.moyenne_teneur_etain()
    all_ventes = sorties.objects.get(id = id)
    form = VenteForm(instance=all_ventes)
    if request.method == 'POST':
        form = VenteForm(request.POST, instance=all_ventes)
        if form.is_valid:
            form.save()
            return redirect('vente_etain')
        

    context = {
        'moyenne_teneur':round(moyenne_teneur,2),
        'all_achats':all_ventes,
        'form':form,
    }
    return render(request, 'pages/ajout_vente_etain.html', context)

def commandes(request):
    all_commande = commande.objects.all()
    stock_c = myClasses()
    moyenne_teneur = stock_c.moyenne_teneur()
    stock_casterie = stock_c.stock_casterie()
    all_ventes = sorties.objects.all().filter(produits_id  = 5)
    stasts = stock_c.stats_all()
    somme_vente = stasts.get("somme_vente")
    somme_achat = stasts.get("somme_achat")
    somme_trans_cast = stasts.get("somme_trans_cast")
    somme_livree_cast =stasts.get("somme_livree_cast") 
    s_qt_non_livree = stasts.get("s_qt_non_livree")
    s_qt_non_livree_etain = stasts.get("s_qt_non_livree_etain")
    s_qt_livree_etain = stasts.get("s_qt_livree_etain")

 
    context = {
        's_qt_non_livree_etain':s_qt_non_livree_etain,
        's_qt_livree_etain':s_qt_livree_etain,
        'moyenne_teneur':round(moyenne_teneur),
        's_qt_non_livree':s_qt_non_livree,
        'somme_livree_cast':somme_livree_cast,
        'somme_trans_cast':somme_trans_cast,
        'somme_achat':somme_achat,
        'somme_vente':somme_vente,
        'stock_casterie':stock_casterie,
        'all_commande':all_commande,
    }
    return render(request, 'pages/commandes.html', context) 

def add_commande(request):
    stock_c = myClasses()
    stock_casterie_etain = stock_c.stock_casterie()
    form = CommandeForm()
    
    
    if request.method == 'POST':
        quantite = request.POST.get("quantite_en_kg")
        form = CommandeForm(request.POST)
        if float(quantite) < stock_casterie_etain:
            if form.is_valid:
                form.save()
                return redirect('commandes')
        else:
             messages.info(request, 'quantite en stock est insuffisante')

        
    context = {
       'form':form,
    }
    return render(request, 'pages/ajout_commande.html', context) 
def update_commande(request,id):
    all_commande = commande.objects.get(id = id)

    stock_c = myClasses()
    stock_casterie_etain = stock_c.stock_casterie()
    
    
    
    form = CommandeForm(instance=all_commande)
    if request.method == 'POST':
        quantite = request.POST.get("quantite")
        form = CommandeForm(request.POST, instance=all_commande)
        
        if float(quantite) < stock_casterie_etain:
            if form.is_valid:
                form.save()
                return redirect('commandes')
        else:
                messages.info(request, 'quantite en stock est insuffisante')

    
    context = {
        'form':form,
    }
    return render(request, 'pages/ajout_commande.html', context) 

