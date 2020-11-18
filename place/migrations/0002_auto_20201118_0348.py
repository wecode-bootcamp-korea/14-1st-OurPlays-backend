# Generated by Django 3.1.3 on 2020-11-18 03:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        ('place', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user'),
        ),
        migrations.AddField(
            model_name='placeimage',
            name='place',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='place.place'),
        ),
        migrations.AddField(
            model_name='place',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='place.category'),
        ),
        migrations.AddField(
            model_name='place',
            name='rating',
            field=models.ManyToManyField(through='place.Rating', to='user.User'),
        ),
        migrations.AddField(
            model_name='place',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_place_user', to='user.user'),
        ),
        migrations.AddField(
            model_name='inavilablebookingday',
            name='place',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='place.place'),
        ),
    ]
