# Generated by Django 3.2.12 on 2022-03-31 17:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_auto_20220331_0912_squashed_0015_auto_20220331_1023'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='teamyear',
            options={'get_latest_by': 'season__year'},
        ),
        migrations.AlterField(
            model_name='league',
            name='code',
            field=models.CharField(blank=True, help_text='Gotten straight from FIRST', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='league',
            name='parentLeague',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='events.league'),
        ),
    ]
