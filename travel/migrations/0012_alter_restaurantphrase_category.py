# Generated by Django 5.1.8 on 2025-07-09 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0011_attraction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurantphrase',
            name='category',
            field=models.CharField(choices=[('general', 'General'), ('ordering', 'Ordering'), ('ingredients', 'Ingredients'), ('emergency', 'Emergency'), ('message', 'E-Card Messages')], default='general', max_length=20),
        ),
    ]
