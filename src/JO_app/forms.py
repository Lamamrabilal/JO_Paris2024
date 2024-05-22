from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Utilisateur, Reservation, Ticket, OffreDeBillet

class UtilisateurCreationForm(UserCreationForm):
    nom = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control my-2',
        'placeholder': "Your Last Name*"
    }))
    
    prenom = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control my-2',
        'placeholder': "Your First Name*"
    }))
    
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': 'form-control my-2',
        'placeholder': "Your Email*"
    }))
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control my-2',
        'placeholder': "Enter Password*"
    }))
    
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control my-2',
        'placeholder': "Confirm Password*"
    }))
    
    class Meta:
        model = Utilisateur
        fields = ['nom', 'prenom', 'email', 'password', 'password_confirm']
   

class UtilisateurLoginForm(AuthenticationForm):
    
    
    class Meta:
        # Exclure le champ 'username'
        model = Utilisateur
        fields = ['email', 'password']
    
class UpdateUtilisateurForm(forms.ModelForm):
    nom = forms.CharField(max_length=100,
                           required=True,
                           widget=forms.TextInput(attrs={'placeholder': 'Nom',
                                                         'class': 'form-control',
                                                         }))
    prenom = forms.CharField(max_length=100,
                              required=True,
                              widget=forms.TextInput(attrs={'placeholder': 'Prénom',
                                                            'class': 'form-control',
                                                            }))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Utilisateur
        fields = ['nom','prenom', 'email']


class UtilisateurProfileForm(forms.ModelForm):
    
    class Meta:
        model = Utilisateur
        fields = ['nom', 'prenom', 'email'] 


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['utilisateur', 'offre_de_billets']  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['offre_de_billets'].queryset = OffreDeBillet.objects.all()

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['reservation','offre_de_billets','qr_code']  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['offre_de_billets'].queryset = OffreDeBillet.objects.all()
