from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .utils import send_email
import random
from installation.models import SiteModel
from .tokens import create_token
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
import jsonfield
from channels.layers import get_channel_layer
import json
from asgiref.sync import async_to_sync
from ckeditor_uploader.fields import RichTextUploadingField
from installation.models import SiteModel
from django.utils.crypto import get_random_string
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import Max
from django.utils.translation import gettext_lazy as _
import environ
from django.contrib.humanize.templatetags.humanize import intcomma,naturaltime
import timeago,datetime
env=environ.Env()
environ.Env.read_env()

     
#generate random
def generate_id():
    return get_random_string(6,'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKMNOPQRSTUVWXYZ0123456789')


#generate random
def generate_serial():
    return get_random_string(12,'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKMNOPQRSTUVWXYZ0123456789')


@receiver(post_save, sender=SiteModel)
def send_installation_email(sender, instance, created, **kwargs):
    if created:
        if instance.is_installed:
            #site is installed
            obj=SiteModel.objects.all()[0]
            subject='Congragulations:Site installed successfully.'
            email=instance.user.email
            message={
                        'user':instance.user,
                        'site_name':instance.site_name,
                        'site_url':instance.site_url,
                        'address':instance.address,
                        'location':instance.location,
                        'description':obj.description,
                        'phone':obj.phone
                     } 
            template='emails/installation.html'
            send_email(subject,email,message,template)





def bgcolor():
    hex_digits=['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
    digit_array=[]
    for i in range(6):
        digits=hex_digits[random.randint(0,15)]
        digit_array.append(digits)
    joined_digits=''.join(digit_array)
    color='#'+joined_digits
    return color





options=[
            ('---Select gender---',
                    (
                        ('Male','Male'),
                        ('Female','Female'),
                        ('Other','Other'),
                    )
            ),
        ]
class ExtendedAuthUser(models.Model):
    user=models.OneToOneField(User,primary_key=True,on_delete=models.CASCADE)
    phone=PhoneNumberField(null=True,blank=True,verbose_name='phone',unique=True,max_length=13)
    initials=models.CharField(max_length=10,blank=True,null=True)
    category=models.CharField(max_length=100,blank=True,null=True)
    serial_no=models.CharField(max_length=100,default=get_random_string,null=True,blank=True)
    bgcolor=models.CharField(max_length=10,blank=True,null=True,default=bgcolor)
    company=models.CharField(max_length=100,null=True,blank=True,default=env('SITE_NAME'))
    zipcode=models.CharField(max_length=100,null=True,blank=True,default='416')
    city=models.CharField(max_length=100,null=True,blank=True,default='Nairobi')
    country=models.CharField(max_length=100,null=True,blank=True,default='Kenya')
    timezone=models.CharField(max_length=200,null=True,blank=True,default='Africa/Nairobi')
    profile_pic=models.ImageField(upload_to='profiles/',null=True,blank=True,default="placeholder.jpg")
    role=models.CharField(choices=[('employee','Employee'),('admins','Admin'),],max_length=200,null=True,blank=True)
    bio=models.TextField(null=True,blank=True,default='something about you...')
    nickname=models.CharField(max_length=100,null=True,blank=True,default='Your nickname')
    facebook=models.CharField(max_length=200,null=True,blank=True,default='https://facebook.com/username')
    twitter=models.CharField(max_length=200,null=True,blank=True,default='https://twitter.com/username')
    instagram=models.CharField(max_length=200,null=True,blank=True,default='https://instagram.com/username')
    linkedin=models.CharField(max_length=200,null=True,blank=True,default='https://linkedin.com/username')
    gender=models.CharField(choices=options,max_length=6,null=True,blank=True)
    birthday=models.DateField(null=True,blank=True)
    created_on=models.DateTimeField(default=now)
    class Meta:
        db_table='extended_auth_user'
        verbose_name_plural='extended_auth_users'
    def __str__(self)->str:
        return f'{self.user.username} extended auth profile'

    def delete(self, using=None,keep_parents=False):
        if self.essay or self.profile_pic or self.certificate:
            self.essay.storage.delete(self.essay.name)
            self.profile_pic.storage.delete(self.profile_pic.name)
            self.certificate.storage.delete(self.certificate.name)
        super().delete()


class MeterModel(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100,blank=True,null=True)
    created_on=models.DateTimeField(default=now)
    class Meta:
        db_table='meter_tbl'
        verbose_name_plural='meter_tbl'
    def __str__(self)->str:
        return f'{self.user.username} meter info'
    def __unicode__(self):
        return self.name


class EquipmentModel(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100,blank=True,null=True)
    created_on=models.DateTimeField(default=now)
    class Meta:
        db_table='equipment_tbl'
        verbose_name_plural='equipment_tbl'
    def __str__(self)->str:
        return f'{self.user.username} equipment info'
    def __unicode__(self):
        return self.name

class ReadingModel(models.Model):
    parent=models.ForeignKey(MeterModel,on_delete=models.CASCADE)
    meter_location=models.CharField(max_length=100,blank=True,null=True)
    meter_reading=models.FloatField(blank=True,null=True)
    date=models.DateField(blank=True,null=True)
    created_on=models.DateTimeField(default=now)
    class Meta:
        db_table='meter_readings_tbl'
        verbose_name_plural='meter_readings_tbl'
    def __str__(self)->str:
        return f'{self.user.username} meter reading info'
    def __unicode__(self):
        return self.parent.name

class CostModel(models.Model):
    year=models.CharField(max_length=100,blank=True,null=True)
    month=models.CharField(max_length=100,blank=True,null=True)
    quantity=models.CharField(max_length=100,blank=True,null=True)
    total_cost=models.FloatField(blank=True,null=True)
    rating=models.FloatField(blank=True,null=True)
    created_on=models.DateTimeField(default=now)
    class Meta:
        db_table='cost_tbl'
        verbose_name_plural='cost_tbl'
    def __str__(self)->str:
        return f'{self.user.username} cost info'
