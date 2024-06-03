# Generated by Django 5.0.6 on 2024-06-03 06:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("scoring", "0003_alter_scoringcategory_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="game",
            name="complexity",
            field=models.IntegerField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(5),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="game",
            name="description",
            field=models.TextField(blank=True, default=""),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="game",
            name="image",
            field=models.URLField(blank=True, default=""),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="game",
            name="max_players",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="game",
            name="max_playtime",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="game",
            name="min_players",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="game",
            name="min_playtime",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="scoringcategory",
            name="description",
            field=models.TextField(blank=True, default=""),
            preserve_default=False,
        ),
    ]
