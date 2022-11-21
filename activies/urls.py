
from django.urls import path
from .views import index, vente, transformation,sortie_etain_brut,updaterecord,updaterecord_bru,sortie_etain,achat
urlpatterns = [
    path('', index, name = 'index' ),
    path('vente/', vente, name = 'vente'),
    path('achat/', achat, name = 'achat'),
    path('transformation/', transformation, name = 'transformation'),
    path('sortir/<int:id>', sortie_etain_brut, name = 'sortie_etain_brut'),
    path('sortir/updaterecord/<int:id>',updaterecord, name='updaterecord'),

    path('sortir_etain/<int:id>', sortie_etain, name = 'updaterecord_bru'),
    path('sortir_etain/updaterecord_bru/<int:id>',updaterecord_bru, name='updaterecord_bru'),
]
