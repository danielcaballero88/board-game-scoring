# Generated by Django 5.0.6 on 2024-06-03 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("scoring", "0005_alter_player_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="player",
            name="nickname",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
