from django.views.generic import ListView, TemplateView
from .models import OffreDeBillet

from django.shortcuts import render
from .models import OffreDeBillet


class Sport:
    def __init__(self, name, image, description):
        self.name = name
        self.image = image
        self.description = description


class HomePageView(TemplateView):
    template_name = 'JO_app/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Récupérer toutes les offres de billets
        offres = OffreDeBillet.objects.all()
        # Créer une liste de sports avec leurs informations
        sports = [
            Sport('Athlétisme', 'images/athletisme.png',
                  "Assistez aux performances incroyables des athlètes les plus rapides et les plus agiles du monde."),
            Sport('Boxe', 'images/boxe.png',
                  "Assistez aux performances incroyables des athlètes de la boxe les plus talentueux du monde."),
            Sport('Natation', 'images/natation.png',
                  "Vivez l'excitation des compétitions de natation avec les nageurs les plus talentueux."),
            Sport('Football', 'images/football.png',
                  "Soyez témoin des moments de gloire sur le terrain de football lors des Jeux Olympiques."),
            # Ajoutez d'autres sports ici
        ]
        # Ajouter les offres et les sports au contexte
        context['offres'] = offres
        context['sports'] = sports
        return context
