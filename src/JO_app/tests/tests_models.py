from django.test import TestCase
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from JO_app.models import Utilisateur, Sport, Site, OffreDeBillet, Reservation, Ticket
import hashlib
import uuid
from io import BytesIO
from PIL import Image
import qrcode
from pyzbar.pyzbar import decode
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

        
class TicketModelTestCase(TestCase):
    def setUp(self):
        
        self.utilisateur = Utilisateur.objects.create_user(
            nom='testuser',
            prenom='testuser',
            email='testuser@example.com',
            password='testpassword',
            clef_1=uuid.uuid4()
        )
        self.sport = Sport.objects.create(name='TestSport')
        self.offre = OffreDeBillet.objects.create(
            type='Solo',
            description='Test description',
            prix=30,
            sport=self.sport
        )
        self.reservation = Reservation.objects.create(
            utilisateur=self.utilisateur,
            offre_de_billets=self.offre,
            clef_2=uuid.uuid4()
        )

    def test_ticket_creation(self):
        ticket = Ticket.objects.create(
            reservation=self.reservation,
            offre_de_billets=self.offre
        )
        self.assertEqual(ticket.reservation, self.reservation)
        self.assertEqual(ticket.offre_de_billets, self.offre)
        self.assertEqual(ticket.clef_finale, 'default_value')

    def test_generer_cle_finale(self):
        ticket = Ticket.objects.create(
            reservation=self.reservation,
            offre_de_billets=self.offre
        )
        ticket.generer_cle_finale()
        expected_clef_finale = hashlib.sha256(
            f"{self.utilisateur.clef_1}-{self.reservation.clef_2}".encode()
        ).hexdigest()
        self.assertEqual(ticket.clef_finale, expected_clef_finale)

    def test_generer_e_billet(self):
        ticket = Ticket.objects.create(
            reservation=self.reservation,
            offre_de_billets=self.offre
        )
        ticket.generer_e_billet()

       
        expected_clef_finale = hashlib.sha256(
            f"{self.utilisateur.clef_1}-{self.reservation.clef_2}".encode()
        ).hexdigest()
        self.assertEqual(ticket.clef_finale, expected_clef_finale)

       
        self.assertTrue(ticket.qr_code.name.startswith('qr_codes/e_billet_'))
        self.assertTrue(ticket.qr_code.name.endswith('.png'))

    def test_qr_code_content(self):
        ticket = Ticket.objects.create(
            reservation=self.reservation,
            offre_de_billets=self.offre
        )
        ticket.generer_e_billet()

        
        ticket.qr_code.open()
        img = Image.open(ticket.qr_code)
        decoded_data = decode(img)
        decoded_clef_finale = decoded_data[0].data.decode('utf-8')

        
        expected_clef_finale = hashlib.sha256(
            f"{self.utilisateur.clef_1}-{self.reservation.clef_2}".encode()
        ).hexdigest()
        self.assertEqual(decoded_clef_finale, expected_clef_finale)