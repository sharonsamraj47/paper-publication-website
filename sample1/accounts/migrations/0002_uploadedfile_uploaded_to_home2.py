# Generated by Django 5.0.6 on 2024-06-22 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedfile',
            name='uploaded_to_home2',
            field=models.BooleanField(default=False),
        ),
    ]
