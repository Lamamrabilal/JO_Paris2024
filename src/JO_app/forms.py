from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Utilisateur, Reservation, Ticket, OffreDeBillet

class UtilisateurCreationForm(UserCreationForm):
    nom = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control my-2',
        'placeholder': "Nom*"
    }))
    
    prenom = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control my-2',
        'placeholder': "Prénom*"
    }))
    
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control my-2',
        'placeholder': "Email*"
    }))
    
    password1 = forms.CharField(label="Mot de Passe", widget=forms.PasswordInput(attrs={
        'class': 'form-control my-2',
        'placeholder': "Mot de Passe*"
    }))
    
    password2 = forms.CharField(label="Confirmer Mot de Passe", widget=forms.PasswordInput(attrs={
        'class': 'form-control my-2',
        'placeholder': "Confirmer Mot de Passe*"
    }))
    
    class Meta:
        model = Utilisateur
        fields = ['nom', 'prenom', 'email', 'password1', 'password2']
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        
        if password1 and password2 and password1 != password2:
            raise ValidationError("Les mots de passe ne correspondent pas")
        
        return cleaned_data


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
    nom_utilisateur = forms.CharField(label='Nom', max_length=100)
    prenom_utilisateur = forms.CharField(label='Prénom', max_length=100)
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
