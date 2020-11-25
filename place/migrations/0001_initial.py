# Generated by Django 3.1.3 on 2020-11-19 07:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'db_table': 'categories',
            },
        ),
        migrations.CreateModel(
            name='InavilableBookingDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField()),
            ],
            options={
                'db_table': 'inavilable_booking_days',
            },
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200)),
                ('price_per_hour', models.IntegerField(default=10000)),
                ('area', models.FloatField(default=0)),
                ('floor', models.IntegerField(default=1)),
                ('maximum_parking_lot', models.IntegerField(default=0)),
                ('allowed_members_count', models.IntegerField(default=1)),
                ('description', models.TextField()),
                ('using_rule', models.TextField()),
                ('info_nearby', models.TextField()),
                ('minimum_rental_hour', models.IntegerField(default=1)),
                ('delegate_place_image_url', models.CharField(max_length=200)),
                ('surcharge_rule', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'places',
            },
        ),
        migrations.CreateModel(
            name='PlaceImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
            ],
            options={
                'db_table': 'place_images',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('places_tags', models.ManyToManyField(to='place.Place')),
            ],
            options={
                'db_table': 'tags',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('starpoint', models.FloatField(default=0)),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_rating_place', to='place.place')),
            ],
            options={
                'db_table': 'ratings',
            },
        ),
    ]
