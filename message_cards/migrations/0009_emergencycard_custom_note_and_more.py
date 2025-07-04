# Generated by Django 5.1.7 on 2025-04-03 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message_cards', '0008_emergencycard_user_name_alter_emergencycard_theme'),
    ]

    operations = [
        migrations.AddField(
            model_name='emergencycard',
            name='custom_note',
            field=models.TextField(blank=True, help_text='Optional: Add a personal note to your emergency card', verbose_name='Personal Note'),
        ),
        migrations.AlterField(
            model_name='emergencycard',
            name='translations',
            field=models.JSONField(blank=True, default=dict, help_text='Stores translations of the custom note', verbose_name='Translations'),
        ),
    ]
