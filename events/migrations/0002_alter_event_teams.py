# Generated by Django 3.2.10 on 2022-01-04 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="teams",
            field=models.ManyToManyField(to="events.TeamYear"),
        ),
    ]
