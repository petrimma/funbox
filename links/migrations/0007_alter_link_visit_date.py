# Generated by Django 3.2.7 on 2021-09-16 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0006_auto_20210913_1430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='visit_date',
            field=models.DateTimeField(verbose_name='Дата посещения'),
        ),
    ]
