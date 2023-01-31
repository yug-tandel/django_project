from django.db import models

# Create your models here.
class BuyerDemo(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    pic = models.FileField(upload_to='buyer_profiles', default= 'avatar.jpg')
    
    def __str__(self) -> str:
        return self.email