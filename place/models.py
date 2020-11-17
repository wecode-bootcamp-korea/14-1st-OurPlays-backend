from django.db import models

class Category(models.Model):
    name                        = models.CharField(max_length=50)
    class Meta:
        db_table = 'categories'

class Place(models.Model):
    address                     = models.CharField(max_length=200)
    price_per_hour              = models.IntegerField(default=10000)
    area                        = models.FloatField(default=0)
    floor                       = models.IntegerField(default=1)
    maximun_parking_lot         = models.IntegerField(default=0)
    allowed_members_count       = models.IntegerField(efault=1)
    description                 = models.TextField()
    using_rule                  = models.TextField()
    info_nearby                 = models.TextField()
    minimum_rental_hour         = models.IntegerField(default=1)
    delegate_place_image_url    = models.CharField(max_length=200)
    surcharge_rule              = models.IntegerField(default=0)
    user                        = models.ForeignKey('user.User',on_delete=models.CASCADE)
    category                    = models.ForeignKey(Category,on_delete=models.CASCADE)
    rating                      = models.ManyToManyField('user.User',through=Rating)
    class Meta:
        db_table = 'places'

class Rating(models.Model):
    starpoint                   = models.FloatField(default=0)
    comment                     = models.TextField()
    created_at                  = models.DateTimeField(auto_now_add=True)
    place                       = models.ForeignKey(Place,on_delete=models.CASCADE)
    user                        = models.ForeignKey('user.User',on_delete=models.CASCADE)
    class Meta:
        db_table = 'ratings'

class PlaceImage(models.Model):
    url                         = models.URLField(max_length=200)
    place                       = models.ForeignKey(Place,on_delete=models.CASCADE)
    class Meta:
        db_table = 'place_images'

class Tag(models.Model):
    name                        = models.CharField(max_length=50)
    created_at                  = models.DateTimeField(auto_now=True)
    places_tags                 = models.ManyToManyField(Place)
    class Meta:
        db_table = 'tags'
        
class InavilableBookingDay(models.Model):
    day                         = models.DateField()
    place                       = models.ForeignKey(Place,on_delete=models.CASCADE)
    class Meta:
        db_table = 'inavilable_booking_days'