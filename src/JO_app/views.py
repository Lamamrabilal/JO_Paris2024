from django.views.generic import ListView
from .models import OffreDeBillet

from django.shortcuts import render
from .models import OffreDeBillet


def HomeView(request):
    # Récupérer toutes les offres de billets
    offres = OffreDeBillet.objects.all()

    # Passez les offres à la template
    context = {'offres': offres}

    # Rendre la template avec les données
    return render(request, 'JO_app/home.html', context)
