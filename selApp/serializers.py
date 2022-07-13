from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers
from selApp.models import Home, ScheduleItemList, City, weather_ackno, ExpiredItemList, AuthToken, PersonInfo, AvailableCity, TotalCity
from rest_framework.authtoken.models import Token

"""def trigger_validator(value):
    if len(value['city']) == 0:
        raise serializers.ValidationError({'phoneNoError': "Please provide valid city"})
"""

class HomeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Home
        fields = ['title', 'description']

class PersonInfoSerializers(serializers.ModelSerializer):
    class Meta:
        model = PersonInfo
        fields = ['name', 'occupation', 'email', 'imageUrl']

class RegisterSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email_id', 'phone', 'city']
        # validators = [trigger_validator]


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ScheduleItemListSerializers(serializers.ModelSerializer):
    class Meta:
        model = ScheduleItemList
        fields = ['id', 'time', 'date', 'scheduleItem', 'lastScheduleOn','pinned', 'user_id']

class ExpiredListSerializers(serializers.ModelSerializer):
    class Meta:
        model = ExpiredItemList
        fields = ['id', 'expired_time', 'expired_date', 'scheduleItem','pinned', 'user_id']


class CitySerializers(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'town', 'user_id']

class WeatherAcknoSerializers(serializers.ModelSerializer):
    class Meta:
        model = weather_ackno
        fields = ['id', 'messages', 'time_of_message', 'messages_alert', 'weatherType', 'maxTemp', 'user_id']

class TokenSerializers(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['user_id']

class AuthTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthToken
        fields = ['id', 'key', 'user_id']
        #read_only_fields = ('key',)

class AvailableCitySerializers(serializers.ModelSerializer):
    class Meta:
        model = AvailableCity
        fields = ['availableCity']

class TotalCitySerializers(serializers.ModelSerializer):
    class Meta:
        model = TotalCity
        fields = ['totalCity']
