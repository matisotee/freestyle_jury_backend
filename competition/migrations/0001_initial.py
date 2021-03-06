# Generated by Django 2.2.16 on 2020-10-20 21:04

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, db_column='_id', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(max_length=25)),
                ('open_inscription_during_competition', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Competitor',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Phase',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Organizer',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, db_column='_id', primary_key=True, serialize=False)),
                ('uid', models.CharField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=25)),
                ('last_name', models.CharField(max_length=25)),
                ('aka', models.CharField(blank=True, max_length=25)),
                ('competitions', djongo.models.fields.ArrayReferenceField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='competition.Competition')),
            ],
        ),
        migrations.AddField(
            model_name='competition',
            name='competitors',
            field=djongo.models.fields.ArrayReferenceField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='competition.Competitor'),
        ),
        migrations.AddField(
            model_name='competition',
            name='phases',
            field=djongo.models.fields.ArrayReferenceField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='competition.Phase'),
        ),
    ]
