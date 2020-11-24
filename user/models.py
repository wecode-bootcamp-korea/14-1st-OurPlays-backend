from django.db    import models

class User(models.Model):
    name                 = models.CharField(max_length=100)
    shoot_count          = models.IntegerField(default=0)
    email                = models.EmailField(max_length=50)
    password             = models.CharField(max_length=300)
    introduce            = models.CharField(max_length=300, default='안녕하세요')
    agree_receive_email  = models.BooleanField(default=False)
    agree_recommand_area = models.BooleanField(default=False)
    thumbnail_url        = models.URLField(max_length=1000, null=True)   
    created_at           = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'users'
        
class Placemark(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    place      = models.ForeignKey('place.Place', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'place_marks'

class UserTag(models.Model):
    keyword            = models.CharField(max_length=45)
    placemark_usertags = models.ManyToManyField(Placemark)

    class Meta:
        db_table = 'user_tags'

class SignupMotive(models.Model):
    user   = models.ForeignKey(User, on_delete=models.CASCADE)
    motive = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'signup_motives'