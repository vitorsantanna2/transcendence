# Generated by Django 5.1.1 on 2024-11-18 23:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='user1',
        ),
        migrations.RemoveField(
            model_name='match',
            name='user1_score',
        ),
        migrations.RemoveField(
            model_name='match',
            name='user2',
        ),
        migrations.RemoveField(
            model_name='match',
            name='user2_score',
        ),
    ]
