from django.forms import ModelForm, TextInput , Select
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *
class CreationUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
class usersForm(ModelForm):
    class Meta:
        model = users
        fields = '__all__'
        exclude = ['user','date_created','name']
class CommandeForm(ModelForm):
    class Meta:
        model = commande
        fields = '__all__'
        exclude = ['date_sortie']
class CommandeForm(ModelForm):
    class Meta:
        model = commande
        fields = '__all__'
        exclude = ['date_sortie','tvaPourcentage']
        
class VenteForm(ModelForm):
    class Meta:
        model = sorties
        fields = '__all__'
        exclude = ['date_sortie','user','tvaPourcentage']

class AchatForm(ModelForm):
    class Meta:
        model = entrees
        fields = '__all__'
        exclude = ['user']
        quantite_template = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=False)

class FondrerieForm(ModelForm):
    class Meta:
        model = transformations
        fields = '__all__'
        exclude = ['user','fourrafine','quantite_entrer_etain_en_kg','quantite_sortie_etain_en_kg','entrant_etain_en_kg','teneur_etain_en_pourcentage']
        quantite_template = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=False) 

class RafinageForm(ModelForm):
    class Meta:
        model = transformations
        fields = '__all__'
        exclude = ['user','fourcasterie','quantite_entrer_casterie_en_kg','quantite_sortie_casterie_en_kg','entrant_casterie_en_kg','teneur_casterie_en_pourcentage','quantite_entrer_etain_en_kg']
        quantite_template = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=False)        

       
 

    

    
    