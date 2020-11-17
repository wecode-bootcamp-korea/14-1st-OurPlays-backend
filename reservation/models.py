from django.db import models

class PayStatus(models.Model):
    reservation_status  = models.CharField(max_length =50)
    class Meta:
        db_table = 'pay_status'

class Reservation(models.Model):
    shooting_members_count = models.IntegerField()
    begin_datetime         = models.DateTimeField()
    finish_datetime        = models.DateTimeField()
    guest_user             = models.ForeignKey('user.User', on_delete   = models.CASCADE)
    place_id               = models.ForeignKey('place.Place', on_delete = models.CASCADE)
    created_at             = models.DateTimeField(auto_now_add          = True)
    status                 = models.ForeignKey(PayStatus, on_delete     = models.CASCADE)
    class Meta:
        db_table = 'reservations'