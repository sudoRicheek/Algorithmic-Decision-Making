# Generated by Django 3.2.4 on 2021-07-23 10:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComprehensionBeliefQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField(blank=True, null=True)),
                ('date_posted', models.DateTimeField(auto_now_add=True, verbose_name='date posted')),
            ],
        ),
        migrations.CreateModel(
            name='ComprehensionBeliefChoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=200)),
                ('is_answer', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.comprehensionbeliefquestion')),
            ],
        ),
    ]