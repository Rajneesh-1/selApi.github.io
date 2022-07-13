from django.contrib import admin
from selApp.models import Home, ScheduleItemList, UserAdditionalInfo, City, weather_ackno, ExpiredItemList, MobileRegistration, AuthToken, MyUser, PersonInfo, AvailableCity, TotalCity

# Register your models here.
@admin.register(Home)
class HomeDetails(admin.ModelAdmin):
    list_display = ['id', 'title', 'description']

@admin.register(PersonInfo)
class PersonInfoDetails(admin.ModelAdmin):
    list_display = ['id', 'name', 'occupation', 'email', 'imageUrl']


@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'email', 'userMobileLinked_id']

@admin.register(MobileRegistration)
class MobileRegistrationAdmin(admin.ModelAdmin):
    list_display = ['id', 'mobileNo', 'otptimeStamp', 'otp']


@admin.register(AuthToken)
class TokenAdmin(admin.ModelAdmin):
    list_display = ['id', 'key', 'user']

@admin.register(ScheduleItemList)
class ScheduleItemListAdmin(admin.ModelAdmin):
    list_display = ['id', 'time', 'date', 'scheduleItem', 'lastScheduleOn','pinned', 'user_id']

@admin.register(ExpiredItemList)
class ExpiredItemListAdmin(admin.ModelAdmin):
    list_display = ['id', 'expired_time', 'expired_date', 'scheduleItem', 'pinned', 'user']


@admin.register(UserAdditionalInfo)
class UserAdditionalInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'fcmToken', 'user']

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['id', 'town', 'user']

@admin.register(weather_ackno)
class Weather_Ackno(admin.ModelAdmin):
    list_display = ['id', 'messages', 'time_of_message', 'messages_alert', 'weatherType', 'maxTemp', 'user']

@admin.register(AvailableCity)
class AvailableCityAdmin(admin.ModelAdmin):
    list_display = ['id', 'availableCity']

@admin.register(TotalCity)
class TotalCityAdmin(admin.ModelAdmin):
    list_display = ['id', 'totalCity']
