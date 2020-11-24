from django.db import models

class ReservationStatus(models.Model):
    status  = models.CharField(max_length=50, unique=True)
    
    class Meta:
        db_table = 'reservation_status'

class Reservation(models.Model):
    shooting_members_count = models.IntegerField(default=0)
    begin_datetime         = models.DateTimeField()
    finish_datetime        = models.DateTimeField()
    guest_user             = models.ForeignKey('user.User', on_delete= models.CASCADE)
    place                  = models.ForeignKey('place.Place', on_delete= models.CASCADE)
    created_at             = models.DateTimeField(auto_now_add= True)
    status                 = models.ForeignKey(ReservationStatus, on_delete= models.CASCADE, default=1)

    class Meta:
        db_table = 'reservations'
