# Generated by Django 3.2.7 on 2021-09-12 14:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='link',
            old_name='link',
            new_name='links',
        ),
    ]
