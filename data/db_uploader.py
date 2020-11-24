import os
import django
import csv
import sys
import bcrypt
import random
from datetime import datetime

from django.db import transaction

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ourplays.settings')
django.setup()

from my_settings import (
                        SECRET_KEY,
                        ALGORITHM
                        )
from user.models import (
                        User,
                        Placemark, 
                        UserTag,
                        SignupMotive,
                        )
from place.models import (
                            Category,
                            Place,
                            Rating,
                            PlaceImage,
                            Tag,
                            InvalidBookingDay,
                            )

CSV_PATH_PLACE = './places.csv'

'''
def gen_regions():
    with open('./regions.csv') as in_file:
        data_reader = csv.reader(in_file)

        regions=[]

        next(data_reader, None)
        for region in data_reader:
            regions.append(Region
'''

@transaction.atomic
def gen_users():
    with open('./users.csv') as in_file:
        data_reader = csv.reader(in_file)

        salt  = bcrypt.gensalt()
        
        next(data_reader, None)
        for row in data_reader:
            User(
                id=int(row[0]),
                name=row[1], 
                email=row[2],
                password=bcrypt.hashpw(row[3].encode(), salt).decode(),
                shoot_count=int(row[4]),
                introduce=row[5],
                agree_receive_email=bool(row[6]),
                agree_recommand_area=bool(row[7]),
                thumbnail_url=row[8],
                )
            
            for motive in row[9].split(','):
                SignupMotive.objects.create(user_id=int(row[0]), motive=motive.trim())
                
            for mark in row[10].split(','):
                Placemark.objects.create(user_id=(row[0]), place_id=int(mark))

@transaction.atomic
def gen_user_tags():
    with open('./users_tag.csv') as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)

        for row in data_reader:
            user_id = User.objects.get(name=row[1]).id
            user_tag = UserTag.objects.create(keyword = row[2])
            for place in row[3].split(','):
                p = Placemark.objects.create(user_id=user_id, place_id=int(place.trim()))
                user_tag.placemark_usertags.add(p) 

@transaction.atomic
def gen_regions():
    with open(CSV_PATH_PLACE) as in_file:
        data_reader = csv.reader(in_file)
        next(data_reader, None)
        '''
        bulk_list = []
        for row in data_reader:
            bulk_list.append(Category(id=int(row[0]), name=row[1]))            
        '''
        Category.objects.bulk_create([Category(id=int(row[0]), name=row[1]) for row in data_reader])

@transaction.atomic
def gen_places():
    with open(CSV_PATH_PLACE) as in_file:
        data_reader = csv.reader(in_file)

        next(data_reader, None)
        
        for row in data_reader:
            place =Place(
                id=int(row[0]),
                address=row[1],
                #region_id=,
                category_id = Category.objects.get(name=row[4]).id,
                user_id = User.objects.get(name=row[5]).id,
                area = float(row[6]),
                floor = int(row[7]),
                maximum_parking_lot = int(row[8]),
                allow_members_count = int(row[9]),
                description=row[10],
                using_rule=row[11],
                info_nearby=row[12],
                minimum_rental_hour=int(row[13]),
                delegate_place_image_url=row[14],
                surcharge_rule=int(row[15])).save()

            for image in row[16].trim().split(','):
                PlaceImage.objects.create(place_id=place.id, url=image) 

            for tag in row[17].trim().split(','):
                tags = Tag.objects.filter(name=tag)
                if not tags:
                    t = Tag.objects.create(name=tag)
                else:
                    t = tags.get()
               
                t.places_tags.add(place)

            for day in row[18].trim().split(','):
                InvalidBookingDay.objects.create(place_id=place.id,
                                                day=datetime.strptime(day, '%Y-%m-%d')
                                                )

            for rate_info in row[19]:
                if rate_info:
                    name, starpoint, comment = rate_info.trim().split(',')
                    user = User.objects.get(name=name)

                    place.rating.add(user)
                    p = place.related_rating_place.get()
                    p.starpoint = float(starpoint)
                    p.comment = comment
                    p.save()
                
@transaction.atomic
def gen_categories():
    with open('./category.csv') as in_file:
        data_reader = csv.reader(in_file)

        next(data_reader, None)
        for row in data_reader:
            Category.objects.create(
                                    id=int(row[0]), 
                                    name=row[1],
                                    )

gen_categories()




