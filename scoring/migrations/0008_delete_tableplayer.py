# Generated by Django 5.0.6 on 2024-06-04 05:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("scoring", "0007_remove_player_nickname_table_owner_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="TablePlayer",
        ),
    ]
