# Generated by Django 5.0.2 on 2024-03-07 22:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Administrateur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_utilisateur', models.CharField(max_length=100)),
                ('mot_de_passe', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='OffreDeBillets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Solo', 'Solo'), ('Duo', 'Duo'), ('Familiale', 'Familiale')], max_length=50)),
                ('description', models.TextField()),
                ('prix', models.DecimalField(decimal_places=2, max_digits=10)),
                ('nombre_ventes', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('adresse_email', models.EmailField(max_length=254, unique=True)),
                ('mot_de_passe', models.CharField(max_length=100)),
                ('clef_securite', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_reservation', models.DateTimeField(auto_now_add=True)),
                ('offre_de_billets', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='JO_app.offredebillets')),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='JO_app.utilisateur')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clef_securite_1', models.CharField(max_length=100)),
                ('clef_securite_2', models.CharField(max_length=100)),
                ('qr_code', models.ImageField(upload_to='qr_codes/')),
                ('offre_de_billets', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='JO_app.offredebillets')),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='JO_app.reservation')),
            ],
        ),
    ]
