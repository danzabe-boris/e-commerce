# Generated by Django 3.2.5 on 2021-09-21 06:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateurs', '0003_remove_article_nom'),
    ]

    operations = [
        migrations.AddField(
            model_name='recherche',
            name='categorie_promo',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
    ]
