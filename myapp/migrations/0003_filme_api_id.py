# Generated by Django 5.0.3 on 2024-04-18 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_filme_myprofile_amigos_myprofile_datadenascimento_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='filme',
            name='api_id',
            field=models.IntegerField(default=0, unique=True),
        ),
    ]
