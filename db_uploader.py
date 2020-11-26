import os
import django
import csv
import sys
import bcrypt
import random
from decimal import Decimal
from datetime import datetime

from django.db import transaction

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ourplays.settings')
django.setup()

from user.models import (
                        User,
                        PlaceMark, 
                        UserTag,
                        SignupMotive,
                        )
from place.models import (
                            Category,
                            Region,
                            Place,
                            Rating,
                            PlaceImage,
                            Tag,
                            InvalidBookingDay,
                            )
from reservation.models import (
                            Reservation,
                            ReservationStatus,
                            )


@transaction.atomic
def gen_users():
    with open('./data/users.csv') as in_file:
        data_reader = csv.reader(in_file)

        salt  = bcrypt.gensalt()
        
        next(data_reader, None)
        User.objects.bulk_create([
                        User(
                            id=int(row[0]),
                            name=row[1], 
                            email=row[2].strip(),
                            password=bcrypt.hashpw(row[3].encode(), salt).decode(),
                            shoot_count=int(row[4]),
                            introduce=row[5],
                            agree_receive_email=bool(row[6]),
                            agree_recommand_area=bool(row[7]),
                            thumbnail_url=row[8],
                            ) for row in data_reader if row[0] and not User.objects.filter(id=int(row[0])).exists()
                        ])
            
        for row in data_reader:
            SignupMotive.objects.bulk_create(
                    [
                            SignupMotive(
                                    user_id=int(row[0]), 
                                    motive=motive.strip()
                            ) for motive in row[9].split(',') if row[0] and not SignupMotive.objects.filter(id=int(row[0]))   
                    ]
            )
                

@transaction.atomic
def gen_user_tags():
    with open('./data/users_tag.csv') as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)

        for row in data_reader:
            user_id = User.objects.get(name=row[1]).id
            user_tag = UserTag.objects.create(keyword = row[2])
            for place in row[3].split(','):
                p = Placemark.objects.create(user_id=user_id, place_id=int(place.strip()))
                user_tag.placemark_usertags.add(p) 

@transaction.atomic
def gen_regions():
    with open('./data/region.csv') as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)
        
        Region.objects.bulk_create([
                Region(
                    id=int(row[0]), 
                    name=row[1]
                    ) for row in data_reader if not Region.objects.filter(name=row[1]).exists()
        ])

@transaction.atomic
def gen_places():
    with open('./data/places.csv') as in_file:
        data_reader = csv.reader(in_file)

        next(data_reader, None)
        Place.objects.bulk_create([
            Place(
                id                       = int(row[0]),
                address                  = row[1],
                region_id                = Region.objects.get(name=row[2]).id,
                category_id              = Category.objects.get(name=row[3]).id,
                user_id                  = User.objects.get(name=row[4]).id,
                price_per_hour           = Decimal(row[5]),
                area                     = float(row[6]),
                floor                    = int(row[7]),
                maximum_parking_lot      = int(row[8]),
                allowed_members_count      = int(row[9]),
                description              = row[10],
                using_rule               = row[11],
                info_nearby              = row[12],
                minimum_rental_hour      = int(row[13]),
                delegate_place_image_url = row[14],
                surcharge_rule           = int(row[15]),
                title                    = row[20],
                ) for row in data_reader if row[0]
            ])

        in_file.seek(0)
        next(data_reader, None)

        place_id = 0
        for row in data_reader:
            if row[0]:
                place_id = int(row[0])

                if row[16]:
                    for image in row[16].split(','):
                        PlaceImage.objects.create(place_id=place_id, url=image.strip()) 

                if row[17]:
                    for tag_name in row[17].split(','):
                        tags = Tag.objects.filter(name=tag_name.strip())
                        if not tags:
                            tag = Tag.objects.create(name=tag_name.strip())
                        else:
                            tag = tags.get()
                       
                        tag.places_tags.add(Place.objects.get(id=place_id))
                        tag.save()

                if row[18]:
                    for day in row[18].split(','):
                        InvalidBookingDay.objects.create(place_id=place_id,
                                                        day=datetime.strptime(day.strip(), '%Y-%m-%d')
                                                        )
            

            if row[19]:
                arr         = row[19].strip().split(',')
                email       = arr[0].strip()
                starpoint   = arr[1].strip()
                comment     = ''
                if len(arr) > 2:
                    comment  = arr[2].strip()

                #print(f'{User.objects.filter(email=email.strip()).values("email")}, {email}')
                
                user  = User.objects.get(email = email)
                place = Place.objects.get(id = place_id)
                place.ratings.add(user)
                
                rating           = Rating.objects.get(place_id = place_id, user_id = user.id)
                rating.starpoint = float(starpoint)
                rating.comment   = comment
                rating.save()

@transaction.atomic
def gen_categories():
    with open('./data/category.csv') as in_file:
        data_reader = csv.reader(in_file)

        next(data_reader, None)
        for row in data_reader:
            if not Category.objects.filter(name=row[1]):
                Category.objects.create(
                                        id=int(row[0]), 
                                        name=row[1],
                                        )

@transaction.atomic
def gen_usertags_and_placemarks():
    with open('./data/users.csv') as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)
        
        placemarks = []
        for row in data_reader:
            if row[0]:
                user_id = int(row[0])

            if row[10]:
                placemarks.append(
                            PlaceMark(
                                user_id  = user_id,
                                place_id = int(row[10])
                                )
                            )

        PlaceMark.objects.bulk_create(placemarks)
        
        in_file.seek(0)
        next(data_reader, None)
        
        for row in data_reader:
            if row[0]:
                user_id = int(row[0])

            if row[11]:                
                for keyword in row[11].split(','):                    
                    user_tags = UserTag.objects.filter(keyword = keyword.strip())                        
                    
                    if not user_tags.exists():
                        user_tag = UserTag.objects.create(
                                        keyword = keyword.strip()
                                    )
                    else:
                        user_tag = user_tags.get()
                        
                    user_tag.placemark.add(PlaceMark.objects.get(user_id = user_id, place_id=int(row[10])))  

def gen_signup_motive():
    with open('./data/signup_motive.csv') as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)

        SignupMotive.objects.bulk_create(
            [
                SignupMotive(
                    user_id = User.objects.get(name=row[1].strip()).id,
                    motive  = motive.strip()
                ) for row in data_reader for motive in row[2].split(',') if row[0]
            ]
        )

def gen_reservation_and_status():
    with open('./data/reservation_status.csv') as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)
        
        ReservationStatus.objects.bulk_create(
            [
                ReservationStatus(
                            status = row[1]
                            ) for row in data_reader if not ReservationStatus.objects.filter(status=row[1]).exists()
            ] 
        )

    with open('./data/reservations.csv') as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)

        Reservation.objects.bulk_create(
            [
                Reservation(
                    place_id = int(row[1]),
                    shooting_members_count = int(row[3]),
                    begin_datetime = datetime.strptime(row[4].strip(), '%Y-%m-%d, %H:%M'),
                    finish_datetime = datetime.strptime(row[5].strip(), '%Y-%m-%d, %H:%M'),
                    guest_user_id = User.objects.get(name=row[2].strip()).id,
                    status_id = ReservationStatus.objects.get(status=row[6].strip()).id,
                ) for row in data_reader
            ]
        )


User.objects.all().delete()
Category.objects.all().delete()
Tag.objects.all().delete()
UserTag.objects.all().delete()

gen_categories()
gen_regions()
gen_users()
gen_places()

gen_usertags_and_placemarks()
gen_signup_motive()

gen_reservation_and_status()




