# Generated by Django 5.1.5 on 2025-03-29 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message_cards', '0007_alter_emergencycard_theme'),
    ]

    operations = [
        migrations.AddField(
            model_name='emergencycard',
            name='user_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='emergencycard',
            name='theme',
            field=models.CharField(choices=[('dark', 'Dark Theme'), ('medical', 'Medical Theme'), ('minimal', 'Minimal Theme')], default='minimal', max_length=20),
        ),
    ]
