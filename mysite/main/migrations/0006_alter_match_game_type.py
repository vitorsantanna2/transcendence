# Generated by Django 5.1.1 on 2024-11-28 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_match_game_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='game_type',
            field=models.CharField(default='local', max_length=50),
        ),
    ]
