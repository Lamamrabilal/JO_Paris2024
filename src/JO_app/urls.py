

import profile
from django.urls import path

from .views import   AjouterAuPanierView, DeconnexionView, HomePageView, ListeOffresView, PayerPanierView, ReservationView, SupprimerDuPanierView,PanierView,connexion, inscription,profile, TicketDownloadView, SportDetailView
from django.contrib.auth import views as auth_views

app_name = "JO_app"

urlpatterns = [
    path('home/', HomePageView.as_view(), name='home'),
    
    path('sport/<int:pk>/', SportDetailView.as_view(), name='detail_sport'),
    path('panier/', PanierView.as_view(), name='panier'),

    path('ajouter_au_panier/<int:offre_id>/', AjouterAuPanierView.as_view(), name='ajouter_au_panier'),
    path('paiement/', PayerPanierView.as_view(), name='paiement'),
    path('supprimer_panier/<int:offre_id>/', SupprimerDuPanierView.as_view(), name='supprimer_panier'),
   
   
    path('inscription/', inscription, name='inscription'),
    path('connexion/', connexion, name='connexion'),
      
    path('compte_utilisateur/', profile, name='compte_utilisateur'),
    path('deconnexion/', DeconnexionView.as_view(), name='deconnexion'),  # Ajout de la vue de déconnexion
   

    path('reservation/',ReservationView.as_view(), name='reservation'),

    path('ticket/<int:reservation_id>/', TicketDownloadView.as_view(), name='ticket'),
   


]

