# Generated by Django 5.0.2 on 2024-04-05 20:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('JO_app', '0003_rename_offredebillets_offredebillet'),
    ]

    operations = [
        migrations.RenameField(
            model_name='utilisateur',
            old_name='est_actif',
            new_name='is_actif',
        ),
        migrations.RenameField(
            model_name='utilisateur',
            old_name='est_staff',
            new_name='is_staff',
        ),
    ]