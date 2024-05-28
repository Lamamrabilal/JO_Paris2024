from django.test import TestCase, Client
from django.urls import reverse
from JO_app.models import OffreDeBillet, Sport, Site, Reservation, Utilisateur,Ticket


class HomePageViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page_view(self):
        response = self.client.get(reverse('JO_app:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'JO_app/home.html')
        self.assertTrue('sports' in response.context)
        self.assertTrue('sites' in response.context)


class SportDetailViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.sport = Sport.objects.create(name="Test Sport", description="Description du sport de test")

    def test_sport_detail_view(self):
        response = self.client.get(reverse('JO_app:detail_sport', args=[self.sport.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'JO_app/detail_sport.html')
        self.assertTrue('sport' in response.context)
        self.assertEqual(response.context['sport'], self.sport)


class PanierViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_panier_view(self):
        response = self.client.get(reverse('JO_app:panier'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'JO_app/panier.html')
        self.assertTrue('offres_du_panier' in response.context)
        self.assertTrue('total_prix' in response.context)

class AjouterAuPanierViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.offre = OffreDeBillet.objects.create(type="Test", prix=50)

    def test_ajouter_au_panier_view(self):
        response = self.client.post(reverse('JO_app:ajouter_au_panier', args=[self.offre.id]))
        self.assertEqual(response.status_code, 302)  # Redirection attendue


class SupprimerDuPanierViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.offre = OffreDeBillet.objects.create(type="Test", prix=50)

    def test_supprimer_du_panier_view(self):
        response = self.client.post(reverse('JO_app:supprimer_panier', args=[self.offre.pk]))
        self.assertEqual(response.status_code, 302)  # Redirection attendue


class PayerPanierViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_payer_panier_view(self):
        response = self.client.post(reverse('JO_app:paiement'))
        self.assertEqual(response.status_code, 302)  # Redirection attendue


class InscriptionViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_inscription_view(self):
        response = self.client.get(reverse('JO_app:inscription'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'JO_app/account/inscription.html')


class ConnexionViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_connexion_view(self):
        response = self.client.get(reverse('JO_app:connexion'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'JO_app/account/connexion.html')


class ProfileViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.utilisateur = Utilisateur.objects.create_user(email='test@example.com', nom='Test', prenom='User', password='password')

    def test_profile_view(self):
        self.client.login(email='test@example.com', password='password')
        response = self.client.get(reverse('JO_app:compte_utilisateur'))
        self.assertEqual(response.status_code,302)
        


class ReservationViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_reservation_view(self):
        response = self.client.get(reverse('JO_app:reservation'))
        self.assertEqual(response.status_code, 302)  # Redirection attendue pour la connexion


class TicketDownloadViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.sport = Sport.objects.create(name='TestSport')
        self.offre = OffreDeBillet.objects.create(type='Test', prix=30, sport=self.sport)
        self.utilisateur = Utilisateur.objects.create_user(email='test@example.com', nom='Test', prenom='User', password='password')

    def test_ticket_download_view(self):
        reservation = Reservation.objects.create(utilisateur=self.utilisateur, offre_de_billets=self.offre)
        ticket = Ticket.objects.create(reservation=reservation, offre_de_billets=self.offre)
        reservation.ticket = ticket
        reservation.save()
        
        url = reverse('JO_app:ticket', args=[reservation.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')