from django.test import TestCase
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from JO_app.models import Utilisateur, Sport, Site, OffreDeBillet, Reservation, Ticket
import uuid
import hashlib

class UtilisateurModelTests(TestCase):
    
    def setUp(self):
        self.utilisateur = Utilisateur.objects.create_user(
            email="test@example.com",
            nom="Test",
            prenom="User",
            mot_de_passe="password123"
        )

    def test_create_user(self):
        user = Utilisateur.objects.get(email="test@example.com")
        self.assertEqual(user.nom, "Test")
        self.assertEqual(user.prenom, "User")

    def test_str_representation(self):
        self.assertEqual(str(self.utilisateur), "Test User")


class SportModelTests(TestCase):
    
    def setUp(self):
        self.sport = Sport.objects.create(
            name="Football",
            image=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg'),
            description="Popular sport"
        )

    def test_create_sport(self):
        sport = Sport.objects.get(name="Football")
        self.assertEqual(sport.description, "Popular sport")

    def test_str_representation(self):
        self.assertEqual(str(self.sport), "Football")


class SiteModelTests(TestCase):
    
    def setUp(self):
        self.site = Site.objects.create(
            name="Stadium",
            image=SimpleUploadedFile(name='test_site_image.jpg', content=b'', content_type='image/jpeg'),
            location="City Center"
        )

    def test_create_site(self):
        site = Site.objects.get(name="Stadium")
        self.assertEqual(site.location, "City Center")

    def test_str_representation(self):
        self.assertEqual(str(self.site), "Stadium")


class OffreDeBilletModelTests(TestCase):
    
    def setUp(self):
        self.sport = Sport.objects.create(
            name="Football",
            image=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg'),
            description="Popular sport"
        )
        self.site = Site.objects.create(
            name="Stadium",
            image=SimpleUploadedFile(name='test_site_image.jpg', content=b'', content_type='image/jpeg'),
            location="City Center"
        )
        self.offre = OffreDeBillet.objects.create(
            type="Solo",
            description="Single ticket",
            prix=50.00,
            sport=self.sport,
            site=self.site
        )

    def test_create_offre_de_billet(self):
        offre = OffreDeBillet.objects.get(description="Single ticket")
        self.assertEqual(offre.prix, 50.00)
        self.assertEqual(offre.sport, self.sport)
        self.assertEqual(offre.site, self.site)

    def ajouter_utilisateurs(self, nombre_utilisateurs):
        if self.type == 'Duo':
            nombre_utilisateurs_a_ajouter = 2 * nombre_utilisateurs
        elif self.type == 'Familiale':
            nombre_utilisateurs_a_ajouter = 4 * nombre_utilisateurs
        else:
            nombre_utilisateurs_a_ajouter = nombre_utilisateurs

        for _ in range(nombre_utilisateurs_a_ajouter):
            Utilisateur.objects.create_user(
                email=f"utilisateur_{Utilisateur.objects.count() + 1}@example.com",
                nom="Nom",
                prenom="Prenom",
                mot_de_passe="defaultpassword"
            )
    def test_ajouter_nouveaux_choix(self):
        initial_choices = len(OffreDeBillet.TYPES_CHOICES)
        OffreDeBillet.ajouter_nouveaux_choix([('Group', 'Group')])
        self.assertEqual(len(OffreDeBillet.TYPES_CHOICES), initial_choices + 1)

    def test_effectuer_vente(self):
        initial_sales = self.offre.nombre_ventes
        self.offre.effectuer_vente()
        self.assertEqual(self.offre.nombre_ventes, initial_sales + 1)


class ReservationModelTests(TestCase):
    
    def setUp(self):
        self.utilisateur = Utilisateur.objects.create_user(
            email="test@example.com",
            nom="Test",
            prenom="User",
            mot_de_passe="password123"
        )
        self.sport = Sport.objects.create(
            name="Football",
            image=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg'),
            description="Popular sport"
        )
        self.site = Site.objects.create(
            name="Stadium",
            image=SimpleUploadedFile(name='test_site_image.jpg', content=b'', content_type='image/jpeg'),
            location="City Center"
        )
        self.offre = OffreDeBillet.objects.create(
            type="Solo",
            description="Single ticket",
            prix=50.00,
            sport=self.sport,
            site=self.site
        )
        self.reservation = Reservation.objects.create(
            utilisateur=self.utilisateur,
            offre_de_billets=self.offre
        )

    def test_reservation_creation(self):
        reservation = Reservation.objects.get(utilisateur=self.utilisateur)
        self.assertEqual(reservation.offre_de_billets, self.offre)

    def test_str_representation(self):
        self.assertEqual(str(self.reservation), str(self.utilisateur))


class TicketModelTests(TestCase):
    
    def setUp(self):
        self.utilisateur = Utilisateur.objects.create_user(
            email="test@example.com",
            nom="Test",
            prenom="User",
            mot_de_passe="password123"
        )
        self.sport = Sport.objects.create(
            name="Football",
            image=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg'),
            description="Popular sport"
        )
        self.site = Site.objects.create(
            name="Stadium",
            image=SimpleUploadedFile(name='test_site_image.jpg', content=b'', content_type='image/jpeg'),
            location="City Center"
        )
        self.offre = OffreDeBillet.objects.create(
            type="Solo",
            description="Single ticket",
            prix=50.00,
            sport=self.sport,
            site=self.site
        )
        self.reservation = Reservation.objects.create(
            utilisateur=self.utilisateur,
            offre_de_billets=self.offre
        )
        self.ticket = Ticket.objects.create(
            reservation=self.reservation,
            offre_de_billets=self.offre
        )

    def test_ticket_creation_and_qr_code_generation(self):
        self.ticket.generer_e_billet()

        self.assertIsNotNone(self.ticket.qr_code)
        self.assertTrue(self.ticket.qr_code.name.startswith("qr_codes/e_billet_"))

    def test_ticket_clef_finale_generation(self):
        self.ticket.generer_cle_finale()
        expected_clef = hashlib.sha256(f"{self.reservation.utilisateur.clef_1}-{self.reservation.clef_2}".encode()).hexdigest()
        self.assertEqual(self.ticket.clef_finale, expected_clef)
