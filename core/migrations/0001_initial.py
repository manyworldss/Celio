# Generated by Django 5.1.8 on 2025-07-09 19:04

import django.core.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EarlyAccessSignup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(help_text='Email address for mobile app notifications', max_length=254, unique=True, validators=[django.core.validators.EmailValidator()])),
                ('name', models.CharField(blank=True, help_text='Optional name of the user', max_length=100)),
                ('wants_updates', models.BooleanField(default=False, help_text='Whether user wants development updates')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, help_text='When the signup was created')),
                ('ip_address', models.GenericIPAddressField(blank=True, help_text='IP address for security tracking', null=True)),
                ('user_agent', models.TextField(blank=True, help_text='Browser user agent for security')),
                ('is_verified', models.BooleanField(default=False, help_text='Whether email has been verified')),
            ],
            options={
                'verbose_name': 'Early Access Signup',
                'verbose_name_plural': 'Early Access Signups',
                'ordering': ['-created_at'],
            },
        ),
    ]
