

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.shortcuts import render, redirect, get_object_or_404,reverse
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
import random

from django.views.generic import ListView, TemplateView, View, DetailView
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib import messages
from .models import Utilisateur,OffreDeBillet, Reservation,Ticket, Sport, Site
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UpdateUtilisateurForm, UtilisateurCreationForm, ReservationForm,TicketForm,UtilisateurCreationForm, UtilisateurLoginForm,UtilisateurProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
import os
import qrcode
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image
from io import BytesIO

class HomePageView(TemplateView):
    template_name = 'JO_app/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        
       
        # Créer une liste de sports avec leurs informations et les prix selon les offres
        sports_data = [
            {
                'name': 'Athlétisme',
                'image': 'images/sports/athletisme.png',
                'description': "Assistez aux performances incroyables des athlètes les plus rapides et les plus agiles du monde."
            },
            {
                'name': 'Boxe',
                'image': 'images/sports/boxe.png',
                'description': "Assistez aux performances incroyables des athlètes de la boxe les plus talentueux du monde."
            },
            {
                'name': 'Natation',
                'image': 'images/sports/natation.png',
                'description': "Vivez l'excitation des compétitions de natation avec les nageurs les plus talentueux."
            },
            {
                'name': 'Football',
                'image': 'images/sports/football.png',
                'description': "Soyez témoin des moments de gloire sur le terrain de football lors des Jeux Olympiques."
            },
            {
                'name': 'Judo',
                'image': 'images/sports/judo_picto.avif',
                'description': "Assistez aux performances incroyables des athlètes les plus rapides et les plus agiles du monde."
            },
            {
                'name': 'Basket',
                'image': 'images/sports/basket_picto.avif',
                'description': "Assistez aux performances incroyables des athlètes de la boxe les plus talentueux du monde."
            },
            {
                'name': 'Volley',
                'image': 'images/sports/volley_picto.avif',
                'description': "Vivez l'excitation des compétitions de natation avec les nageurs les plus talentueux."
            },
            {
                'name': 'Tennis',
                'image': 'images/sports/tennis_picto.avif',
                'description': "Soyez témoin des moments de gloire sur le terrain de football lors des Jeux Olympiques."
            }
        ]

        # Enregistrer ou mettre à jour les sports
        for sport_data in sports_data:
            sport, created = Sport.objects.get_or_create(
                name=sport_data['name'],
                defaults={
                    'image': sport_data['image'],
                    'description': sport_data['description']
                }
            )
            if not created:
                # Mettre à jour les champs si le sport existe déjà
                sport.image = sport_data['image']
                sport.description = sport_data['description']
                sport.save()

            # Ajouter les offres de billets à chaque sport
            OffreDeBillet.objects.get_or_create(type='Solo', prix=30, sport=sport)
            OffreDeBillet.objects.get_or_create(type='Duo', prix=50, sport=sport)
            OffreDeBillet.objects.get_or_create(type='Familiale', prix=100, sport=sport)

        # Créer une liste de sites des Jeux Olympiques de Paris avec leurs informations
        sites_data = [
            {
                'name': 'Stade Olympique',
                'image': 'images/sites_olympique/stade_de_France.avif',
                'location': 'Paris'
            },
            {
                'name': 'Les invalides',
                'image': 'images/sites_olympique/Invalides.png',
                'location': 'Paris'
            },
            {
                'name': 'Stade Tour Eiffel',
                'image': 'images/sites_olympique/stade_tour_Eiffel.png',
                'location': 'Paris'
            },
             {
                'name': 'Chateau de Versaille',
                'image': 'images/sites_olympique/Chateau_versaille.png',
                'location': 'Paris'
            },
            {
                'name': 'Stade de Marseille',
                'image': 'images/sites_olympique/Stade de Marseille.jpg',
                'location': 'Marseille'
            },
            {
                'name': 'Stade Pierre Mauroy',
                'image': 'images/sites_olympique/Stade Pierre Mauroy.jpg',
                'location': 'Lille'
            }

        ]

        # Enregistrer ou mettre à jour les sites
        for site_data in sites_data:
            Site.objects.get_or_create(
                name=site_data['name'],
                defaults={
                    'image': site_data['image'],
                    'location': site_data['location']
                }
            )

        # Récupérer les sports et les sites depuis la base de données
        context['sports'] = Sport.objects.all()
        context['sites'] = Site.objects.all()
        
        return context



class ListeOffresView(ListView):
    model = OffreDeBillet
    
    context_object_name = 'offres'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['offres'] = OffreDeBillet.objects.all()
        
        return context
class SportDetailView(DetailView):
    model = Sport
    template_name = 'JO_app/detail_sport.html'
    context_object_name = 'sport'



class PanierView(TemplateView):
    template_name = 'JO_app/panier.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        panier_ids = self.request.session.get('panier', [])
        offres_du_panier = OffreDeBillet.objects.filter(pk__in=panier_ids)
        
        # Calculer le montant total du panier
        total_prix = sum(offre.prix for offre in offres_du_panier)

        context['offres_du_panier'] = offres_du_panier
        context['total_prix'] = total_prix  # Ajouter le montant total au contexte
        return context

    def post(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class AjouterAuPanierView(View):
    def post(self, request, offre_id):
        offre = get_object_or_404(OffreDeBillet, pk=offre_id)
        panier = request.session.get('panier', [])

        if offre_id not in panier:
            panier.append(offre_id)
            request.session['panier'] = panier
            request.session.modified = True  # Marquer la session comme modifiée
            messages.success(request, 'Offre ajoutée au panier avec succès !')
        else:
            messages.info(request, 'Cette offre est déjà dans votre panier.')

        return redirect('JO_app:panier')

    def get(self, request, offre_id):
        return redirect('JO_app:panier')

        
class SupprimerDuPanierView(View):
    def post(self, request, offre_id):
        
        panier = request.session.get('panier', [])
        if offre_id in panier:
            panier.remove(offre_id)
            request.session['panier'] = panier
            messages.success(request, 'Offre supprimée du panier avec succès !')
        else:
            messages.error(request, 'Cette offre n\'est pas dans votre panier.')
        return redirect('JO_app:panier')  



class PayerPanierView(View):
    def post(self, request):
        if self.simuler_paiement():
            messages.success(request, 'Paiement réussi !')
            self.creer_reservation(request)
            self.vider_panier(request)
        else:
            messages.error(request, 'Échec du paiement. Veuillez réessayer plus tard.')
        return redirect('JO_app:panier')

    def simuler_paiement(self):
        return random.random() < 0.8  # Simule un paiement réussi avec 80% de probabilité

    def creer_reservation(self, request):
        panier = request.session.get('panier')
        if panier:
            for offre_id in panier:
                offre = OffreDeBillet.objects.get(id=offre_id)
                reservation = Reservation.objects.create(utilisateur=request.user, offre_de_billets=offre)

                # Ajouter les noms des utilisateurs en fonction du type d'offre
                noms_utilisateurs = request.POST.getlist('noms_utilisateurs')
                reservation.noms_utilisateurs = noms_utilisateurs
                reservation.save()

                # Effectuer la vente
                offre.effectuer_vente()

                # Génération du billet
                ticket = Ticket.objects.create(reservation=reservation, offre_de_billets=offre)
                reservation.ticket = ticket
                reservation.save()
                ticket.generer_e_billet()

                # Envoi d'un e-mail de confirmation
                subject = 'Confirmation de réservation'
                message = f'Votre réservation a été confirmée. ID de réservation : {reservation.utilisateur}'
                send_mail(subject, message, settings.EMAIL_HOST_USER, [request.user.email])

    def vider_panier(self, request):
        if 'panier' in request.session:
            del request.session['panier']

    def envoyer_email_confirmation(self, reservation):
        subject = 'Confirmation de réservation'
        message = f'Votre réservation a été confirmée. ID de réservation : {reservation.id}'
        recipient = reservation.utilisateur.email

        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        try:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, recipient, msg.as_string())
            server.quit()
            print("Email envoyé avec succès")
        except Exception as e:
            print(f"Erreur lors de l'envoi de l'email: {e}")


def inscription(request):
    if request.method == 'POST':
        form = UtilisateurCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('JO_app:connexion')
    else:
        form = UtilisateurCreationForm()
    return render(request, 'JO_app/account/inscription.html', {'form': form})

def connexion(request):
    if request.method == 'POST':
        form = UtilisateurLoginForm(data=request.POST)
        
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            print("User:", user)  # Ajoutez cette ligne pour afficher l'utilisateur authentifié
            if user is not None:
                login(request, user)
                print("User is authenticated:", request.user.is_authenticated)  # Ajoutez cette ligne pour vérifier si l'utilisateur est authentifié
                return redirect('JO_app:home')
    else:
        form = UtilisateurLoginForm()
    return render(request, 'JO_app/account/connexion.html', {'form': form})


class DeconnexionView(View):
    def get(self, request):
        logout(request)
        return redirect('JO_app:home')  # Rediriger vers la page d'accueil après déconnexion


@login_required
def profile(request):
    utilisateur = request.user
    
    if request.method == 'POST':
        form =UpdateUtilisateurForm(request.POST, instance=utilisateur)
        if form.is_valid():
            form.save()
            return redirect('JO_app:home')
    else:
        form =UpdateUtilisateurForm(instance=utilisateur)
    
    return render(request, 'JO_app/account/compte_utilisateur.html', {'form': form})


class ReservationView(LoginRequiredMixin, View):
    login_url = 'JO_app:connexion'

    def get(self, request):
        reservations = Reservation.objects.filter(utilisateur=request.user)
        form = ReservationForm()
        return render(request, 'JO_app/reservation.html', {'form': form, 'reservations': reservations})

    def post(self, request):
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.utilisateur = request.user
            reservation.save()

            ticket = Ticket.objects.create(reservation=reservation, offre_de_billets=reservation.offre_de_billets)
            reservation.ticket = ticket
            reservation.save()

            return redirect('JO_app:home')

class TicketDownloadView(View):
    
    def get(self, request, reservation_id):
        try:
            reservation = Reservation.objects.get(id=reservation_id)
        except Reservation.DoesNotExist:
            return HttpResponse(status=404)
        
        if not hasattr(reservation, 'ticket'):
            return HttpResponseNotFound("Ticket non disponible")

        # Créer un objet BytesIO pour stocker le PDF en mémoire
        buffer = BytesIO()

        # Créer un document PDF
        pdf = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        # Ajouter le contenu au PDF
        ticket = reservation.ticket
        data = [
            ["Nom", reservation.utilisateur.nom],
            ["Prénom", reservation.utilisateur.prenom],
            ["Noms des utilisateurs", ", ".join([user.nom if hasattr(user, 'nom') else user for user in reservation.noms_utilisateurs])],
            ["Événement", reservation.offre_de_billets.type],  # Correction ici
            ["Épreuve", reservation.offre_de_billets.sport],  # Correction ici
            ["Date", reservation.date_reservation.strftime('%d-%m-%Y')],
        ]

        # Créer une table pour stocker les informations
        table = Table(data, colWidths=[150, 200])

        # Appliquer un style à la table
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#009F3D")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#009F3D")),
        ])
        table.setStyle(style)

        # Générer le code QR
        qr = qrcode.make(f"ID de réservation : {reservation_id}", box_size=10)
        qr_img = BytesIO()
        qr.save(qr_img)
        qr_img.seek(0)

        # Ajouter le code QR au PDF
        qr_code_image = Image(qr_img)
        qr_code_image.drawHeight = 50
        qr_code_image.drawWidth = 150

        # Créer un tableau avec le QR code et les informations utilisateur côte à côte
        combined_data = [
            [qr_code_image, table]
        ]
        combined_table = Table(combined_data, colWidths=[150, 400])

        # Ajouter le tableau combiné aux éléments du PDF
        elements.append(combined_table)

        # Construire le PDF
        pdf.build(elements)

        # Retourner le PDF en tant que réponse HTTP
        buffer.seek(0)
        response = HttpResponse(buffer.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="billet_{reservation.id}.pdf"'
        return response