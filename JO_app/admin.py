

from django.db.models import Count
from django.contrib import admin
from .models import Utilisateur, OffreDeBillet, Reservation, Ticket


@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'email', 'clef_1')
    search_fields = ('nom', 'prenom', 'email')


@admin.register(OffreDeBillet)
class OffreDeBilletAdmin(admin.ModelAdmin):
    list_display = ('type', 'description', 'prix', 'nombre_ventes')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(total_ventes=Count('reservation__id'))
        return queryset

    def nombre_ventes(self, obj):
        return obj.total_ventes
    nombre_ventes.admin_order_field = 'total_ventes'

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'offre_de_billets',
                    'date_reservation', 'clef_2')

    def save_model(self, request, obj, form, change):
   
        obj.offre_de_billets.nombre_ventes += 1
        obj.offre_de_billets.save()
        super().save_model(request, obj, form, change)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('reservation', 'offre_de_billets',
                    'clef_finale', 'qr_code')
