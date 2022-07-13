from datetime import datetime

import pytz
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class Home(models.Model):
    title = models.CharField(max_length=100, default="")
    description = models.CharField(max_length=100, default="")


class PersonInfo(models.Model):
    name = models.CharField(max_length=20)
    occupation = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    imageUrl = models.CharField(max_length=1000)


class MobileRegistration(models.Model):
    mobileNo = models.CharField(max_length=10)
    otptimeStamp = models.CharField(max_length=100)
    otp = models.CharField(max_length=100)


class MyUser(AbstractUser):
    userMobileLinked = models.ForeignKey(MobileRegistration, on_delete=models.CASCADE, null=True)
    # date_of_birth = models.DateField()
    # height = models.FloatField()
    # REQUIRED_FIELDS = ['date_of_birth', 'height']


class ScheduleItemList(models.Model):
    user = models.ForeignKey(MobileRegistration, on_delete=models.CASCADE, related_name="user")
    time = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    scheduleItem = models.CharField(max_length=1000)
    pinned = models.CharField(default=0, max_length=1)
    lastScheduleOn = models.CharField(default=datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%d-%m-%Y'),
                                      max_length=200)


class ExpiredItemList(models.Model):
    user = models.ForeignKey(MobileRegistration, on_delete=models.CASCADE)
    expired_time = models.CharField(max_length=100)
    expired_date = models.CharField(max_length=100)
    scheduleItem = models.CharField(max_length=1000)
    pinned = models.CharField(default=0, max_length=1)


class weather_ackno(models.Model):
    user = models.ForeignKey(MobileRegistration, on_delete=models.CASCADE)
    messages = models.CharField(default=1, max_length=10000)
    time_of_message = models.CharField(default=0, max_length=1000)
    messages_alert = models.CharField(default=0, max_length=1)
    weatherType = models.CharField(default=0, max_length=20)
    maxTemp = models.CharField(default=0, max_length=10)


class City(models.Model):
    user = models.ForeignKey(MobileRegistration, on_delete=models.CASCADE)
    town = models.CharField(max_length=40)


class UserAdditionalInfo(models.Model):
    user = models.ForeignKey(MobileRegistration, on_delete=models.CASCADE)
    fcmToken = models.CharField(max_length=200)


class AuthToken(models.Model):
    user = models.ForeignKey(MobileRegistration, on_delete=models.CASCADE)
    key = models.CharField(verbose_name='Key', max_length=40)

    '''
    class Meta:
        verbose_name = 'Token'
        verbose_name_plural = 'Tokens'

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.keyS
    '''


class AvailableCity(models.Model):
    availableCity = models.CharField(max_length=40)


class TotalCity(models.Model):
    totalCity = models.CharField(max_length=1000000)


""" for web models """
from django.db import models
from django.db.models.fields import CharField, IntegerField
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime
import pytz


class Image(models.Model):
    photo = models.ImageField(upload_to='pictures')
    date = models.DateTimeField(auto_now_add=True)


class Room(models.Model):
    user_inv = models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True)
    Room_name = models.CharField(max_length=1000)


class user_involved(models.Model):
    Room_ka_name = models.CharField(max_length=1000)
    user_ka_name = models.CharField(max_length=1000)


class Grp_admin(models.Model):
    related_room = models.OneToOneField(Room, on_delete=models.CASCADE, primary_key=True)
    G_a = models.CharField(max_length=1000)
    preference = models.CharField(max_length=10)
    he_is_adm_of = models.CharField(max_length=1000)


class Message(models.Model):
    message_content = models.CharField(max_length=1000000)
    message_date = models.CharField(default=0, max_length=1000)
    user = models.CharField(max_length=1000000)
    belongs_to_room = models.CharField(max_length=1000000)


class seen(models.Model):
    users_ka_name = models.CharField(max_length=10000)
    special_id = models.CharField(max_length=10000)
    roomnm = models.CharField(default=0, max_length=10000)
    time_of_reject = models.CharField(default=0, max_length=1000)


class waiting_users(models.Model):
    name_of_room = models.CharField(max_length=1000)
    users_message = models.CharField(max_length=1000)
    users_name = models.CharField(max_length=1000)


'''class weather_ackno(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    messages = models.CharField(default=1,max_length=10000)
    time_of_message=models.CharField(default=0,max_length=1000)
    messages_alert = models.CharField(default=0,max_length=1)
'''


class Selectoptions(models.Model):
    def validate_ukey(uk):
        if not 6 < len(uk) < 21:
            raise ValidationError(
                'Unique Key Must be ( in b/w 6 ~ 21) of character, Your was of ' + str(len(uk)) + ' character.')

    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True)
    city_name = models.CharField(max_length=70)
    phone_no = PhoneNumberField()
    unique_key = models.CharField(default=0, max_length=100, validators=[validate_ukey])
    incr = models.CharField(default=1, max_length=1)
    date_time = models.CharField(default=1, max_length=30)
    combKey = models.CharField(default=1, max_length=5)
    time_check = models.CharField(default=1, max_length=30)


class Scheduled(models.Model):
    def validate_time(schedule_time):
        x = datetime.now(pytz.timezone('Asia/Kolkata'))
        # print("datetime.now() :",datetime.now())
        # print("type(datetime.now()) :",type(datetime.now()))
        x = x.strftime('%H:%M:%S')
        # print("x.strftime('%H:%M:%S') :",x)
        x = datetime.strptime(x, '%H:%M:%S')
        # print("datetime.datetime.strptime(x,'%H:%M:%S')",x)
        y = schedule_time
        # print("schedule_time",schedule_time)
        y = y.strftime('%H:%M:%S')
        # print("y.strftime('%H:%M:%S') :",y)
        y = datetime.strptime(y, '%H:%M:%S')
        # print("datetime.datetime.strptime(x,'%H:%M:%S')", y)

        c = x - y
        # print("c :",c)
        # print("type(c) :",type(c))

        if c.total_seconds() < 0:
            pass
        else:
            raise ValidationError("Oye ! Schedule Time cannot be in the Past")

    def validate_date(date):
        if date < timezone.now().date():
            raise ValidationError("Oye ! Schedule Date cannot be in the Past")

    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    schedule_items = models.TextField()
    schedule_date = models.DateField(validators=[validate_date])
    schedule_time = models.TimeField(validators=[validate_time])

    # = models.DateTimeField()


class Pin_Unpin(models.Model):
    pin_id = IntegerField()
    pin_ka_id = CharField(max_length=1000)
    pin_permission = CharField(max_length=20)


class capture_schedule(models.Model):
    cap_sch = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    capture_schedule_time = models.CharField(max_length=100)


class expired_scheduledList(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    schedule_items = models.TextField()
    schedule_date = models.DateField()
    schedule_time = models.TimeField()
