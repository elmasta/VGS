# Generated by Django 3.0.3 on 2020-03-06 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0004_auto_20200306_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userownedgame',
            name='rating',
            field=models.IntegerField(blank=True, choices=[(1, 'Zero'), (2, 'Un'), (3, 'Deux'), (4, 'Trois'), (5, 'Quatre'), (6, 'Cinq'), (7, 'Six'), (8, 'Sept'), (9, 'Huit'), (10, 'Neuf'), (11, 'Dix')], null=True),
        ),
        migrations.AlterField(
            model_name='userownedgamedlc',
            name='rating',
            field=models.IntegerField(blank=True, choices=[(1, 'Zero'), (2, 'Un'), (3, 'Deux'), (4, 'Trois'), (5, 'Quatre'), (6, 'Cinq'), (7, 'Six'), (8, 'Sept'), (9, 'Huit'), (10, 'Neuf'), (11, 'Dix')], null=True),
        ),
    ]