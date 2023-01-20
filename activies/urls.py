
from django.urls import path
from . import views
urlpatterns = [
    # la partie initiale 
    path('', views.index, name = 'index' ),
    path('login/', views.loginpage, name = 'login'),
    path('logout/', views.logoutpage, name = 'logout'),
    path('createUser/', views.createUser, name = 'createUser'),
    path('user_profil/', views.user_profil, name = 'user_profil'),

    path('achat/', views.Achat, name = 'achat'),
    path('add_Achat/', views.add_Achat, name = 'add_Achat'),
    path('update_achat/<int:id>', views.update_achat, name = 'update_achat'),
    path('facture/<int:id>', views.facture, name = 'facture'),

    path('vente/', views.vente, name = 'vente'),
    path('add_vente/', views.add_vente, name = 'add_vente'),
    path('update_vente<int:id>', views.update_vente, name = 'update_vente'),
    
    path('vente_etain/', views.vente_etain, name = 'vente_etain'),
    path('add_vente_etain/', views.add_vente_etain, name = 'add_vente_etain'),
    path('update_vente_etain/<int:id>', views.update_vente_etain, name = 'update_vente_etain'),

    path('commandes/', views.commandes, name = 'commandes'),
    path('add_commande/', views.add_commande, name = 'add_commande'),
    path('update_commande/<int:id>', views.update_commande, name = 'update_commande'),

    path('fondrerie/', views.fondrerie, name = 'fondrerie'),
    path('add_fondre/', views.add_fondre, name = 'add_fondre'),
    path('update_fondre/<int:id>', views.update_fondre, name = 'update_fondre'),

    path('rafinage/', views.rafinage, name = 'rafinage'),
    # path('add_rafinage/', views.add_rafinage, name = 'add_rafinage'),
    path('update_rafinage/<int:id>', views.update_rafinage, name = 'update_rafinage'),


  
]
