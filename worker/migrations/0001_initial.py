# Generated by Django 3.2.4 on 2021-06-03 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('question', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('worker_id', models.CharField(max_length=200, unique=True)),
                ('responses', models.ManyToManyField(to='question.ChoiceOptions')),
            ],
        ),
    ]