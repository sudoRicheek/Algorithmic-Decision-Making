# Generated by Django 3.2.4 on 2021-07-28 08:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PostExperimentalChoice',
        ),
        migrations.DeleteModel(
            name='PostExperimentalQuestion',
        ),
    ]
