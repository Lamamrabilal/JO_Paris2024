from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import AjouterAuPanierView, DeconnexionView, HomePageView, PayerPanierView, ReservationView, SupprimerDuPanierView, PanierView, connexion, inscription, profile, TicketDownloadView, SportDetailView

class TestUrls(SimpleTestCase):

    def test_home_url_resolves(self):
        url = reverse('JO_app:home')
        self.assertEqual(resolve(url).func.view_class, HomePageView)

    def test_detail_sport_url_resolves(self):
        url = reverse('JO_app:detail_sport', args=[1])
        self.assertEqual(resolve(url).func.view_class, SportDetailView)

    def test_panier_url_resolves(self):
        url = reverse('JO_app:panier')
        self.assertEqual(resolve(url).func.view_class, PanierView)

    def test_ajouter_au_panier_url_resolves(self):
        url = reverse('JO_app:ajouter_au_panier', args=[1])
        self.assertEqual(resolve(url).func.view_class, AjouterAuPanierView)

    def test_paiement_url_resolves(self):
        url = reverse('JO_app:paiement')
        self.assertEqual(resolve(url).func.view_class, PayerPanierView)

    def test_supprimer_panier_url_resolves(self):
        url = reverse('JO_app:supprimer_panier', args=[1])
        self.assertEqual(resolve(url).func.view_class, SupprimerDuPanierView)

    def test_inscription_url_resolves(self):
        url = reverse('JO_app:inscription')
        self.assertEqual(resolve(url).func, inscription)

    def test_connexion_url_resolves(self):
        url = reverse('JO_app:connexion')
        self.assertEqual(resolve(url).func, connexion)

    def test_compte_utilisateur_url_resolves(self):
        url = reverse('JO_app:compte_utilisateur')
        self.assertEqual(resolve(url).func, profile)

    def test_deconnexion_url_resolves(self):
        url = reverse('JO_app:deconnexion')
        self.assertEqual(resolve(url).func.view_class, DeconnexionView)

    def test_reservation_url_resolves(self):
        url = reverse('JO_app:reservation')
        self.assertEqual(resolve(url).func.view_class, ReservationView)

    def test_ticket_url_resolves(self):
        url = reverse('JO_app:ticket', args=[1])
        self.assertEqual(resolve(url).func.view_class, TicketDownloadView)
