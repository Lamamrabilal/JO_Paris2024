from django.test import TestCase
from django.contrib.auth import get_user_model
from ..forms import UtilisateurCreationForm, UtilisateurLoginForm, UpdateUtilisateurForm, UtilisateurProfileForm, ReservationForm, TicketForm
from ..models import Utilisateur, OffreDeBillet, Reservation, Ticket
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io



class TestUtilisateurCreationForm(TestCase):
    
    def test_valid_form(self):
        form_data = {
            'nom': 'Doe',
            'prenom': 'John',
            'email': 'johndoe@example.com',
            'password1': 'MyStrongPassword123',
            'password2': 'MyStrongPassword123'
        }
        form = UtilisateurCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            'nom': '',
            'prenom': 'John',
            'email': 'invalid-email',
            'password1': 'password123',
            'password2': 'password123'
        }
        form = UtilisateurCreationForm(data=form_data)
        
        # Affiche les erreurs de validation si le formulaire n'est pas valide
        if not form.is_valid():
            print(form.errors.as_data())
        
        self.assertFalse(form.is_valid())


class UtilisateurLoginFormTest(TestCase):
    def setUp(self):
        self.user = Utilisateur.objects.create_user(
            email="test@example.com",
            nom="Test",
            prenom="User",
            mot_de_passe="password123"
        )

    def test_valid_login_form(self):
        form_data = {
            'username': 'test@example.com',
            'password': 'password123',
        }
        form = UtilisateurLoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_login_form(self):
        form_data = {
            'username': 'test@example.com',
            'password': 'wrongpassword',
        }
        form = UtilisateurLoginForm(data=form_data)
        self.assertFalse(form.is_valid())


class UpdateUtilisateurFormTest(TestCase):
    def setUp(self):
        self.user = Utilisateur.objects.create_user(
            email="test@example.com",
            nom="Test",
            prenom="User",
            mot_de_passe="password123"
        )

    def test_valid_update_form(self):
        form_data = {
            'nom': 'Updated',
            'prenom': 'User',
            'email': 'updated@example.com',
        }
        form = UpdateUtilisateurForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())
        updated_user = form.save()
        self.assertEqual(updated_user.nom, 'Updated')
        self.assertEqual(updated_user.email, 'updated@example.com')


class UtilisateurProfileFormTest(TestCase):
    def setUp(self):
        self.user = Utilisateur.objects.create_user(
            email="test@example.com",
            nom="Test",
            prenom="User",
            mot_de_passe="password123"
        )

    def test_valid_profile_form(self):
        form_data = {
            'nom': 'Profile',
            'prenom': 'User',
            'email': 'profile@example.com',
        }
        form = UtilisateurProfileForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())
        updated_user = form.save()
        self.assertEqual(updated_user.nom, 'Profile')
        self.assertEqual(updated_user.email, 'profile@example.com')


class ReservationFormTest(TestCase):
    def setUp(self):
        self.user = Utilisateur.objects.create_user(
            email="test@example.com",
            nom="Test",
            prenom="User",
            mot_de_passe="password123"
        )
        self.offre = OffreDeBillet.objects.create(
            type="Solo",
            description="Single ticket",
            prix=50.00,
        )

    def test_valid_reservation_form(self):
        form_data = {
            'utilisateur': self.user.id,
            'offre_de_billets': self.offre.id,
            'nom_utilisateur': 'Reservation',
            'prenom_utilisateur': 'Test',
        }
        form = ReservationForm(data=form_data)
        self.assertTrue(form.is_valid())
        reservation = form.save()
        self.assertEqual(reservation.utilisateur, self.user)
        self.assertEqual(reservation.offre_de_billets, self.offre)


class TicketFormTest(TestCase):
    def setUp(self):
        self.utilisateur = Utilisateur.objects.create_user(nom='Doe', prenom='John', email='johndoe@example.com', password='MyStrongPassword123')
        self.offre_de_billet = OffreDeBillet.objects.create(type='Concert', prix=100.0)
        self.reservation = Reservation.objects.create(utilisateur=self.utilisateur, offre_de_billets=self.offre_de_billet)

    def test_valid_ticket_form(self):
        # Créer une image en mémoire
        image = Image.new('RGB', (100, 100), color = (73, 109, 137))
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        uploaded_file = SimpleUploadedFile("qr_code.png", img_byte_arr.read(), content_type="image/png")

        form_data = {
            'reservation': self.reservation.id,
            'offre_de_billets': self.offre_de_billet.id
        }
        form_files = {'qr_code': uploaded_file}
        form = TicketForm(data=form_data, files=form_files)
        print(form.errors)  # Affiche les erreurs de validation du formulaire pour diagnostic
        self.assertTrue(form.is_valid())
