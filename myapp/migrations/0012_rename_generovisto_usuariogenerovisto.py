# Generated by Django 5.0.3 on 2024-07-11 01:35

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_rename_usuariogenerovisto_generovisto'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='GeneroVisto',
            new_name='UsuarioGeneroVisto',
        ),
    ]
