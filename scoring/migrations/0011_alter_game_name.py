# Generated by Django 5.0.6 on 2024-06-05 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("scoring", "0010_alter_player_favorite_games"),
    ]

    operations = [
        migrations.AlterField(
            model_name="game",
            name="name",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
