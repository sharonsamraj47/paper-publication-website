# Generated by Django 5.0.6 on 2024-07-16 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_uploadedfile_uploaded_to_home2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedfile',
            name='uploaded_to_home2',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
    ]
