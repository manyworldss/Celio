# Generated by Django 5.1.8 on 2025-07-02 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0002_add_initial_countries'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='color',
            field=models.CharField(default='#808080', max_length=7),
        ),
    ]
