# Generated by Django 5.1.8 on 2025-07-08 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0008_add_ecard_countries'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='color',
            field=models.CharField(default='#808080', help_text='Hex color code for the country card', max_length=7),
        ),
    ]
