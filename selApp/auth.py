from django.contrib.auth.models import update_last_login
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import UserAdditionalInfo, City, weather_ackno

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data= request.data, context={'request': request})
        try:
            serializer.is_valid(raise_exception=False)
            user = serializer.validated_data['user']
        except:
            return Response({'responseCode': 110, 'responseMessage': 'Wrong Username/Password'})

        update_last_login(None, user)
        print("user:", user)

        fcmTokenValue = request.META.get('HTTP_AUTHORIZATION', b'')
        print("fcmTokenValue:", fcmTokenValue)

        userAdditionalInfo = UserAdditionalInfo.objects.filter(user_id=user.id)
        print("userAdditionalInfo: ",userAdditionalInfo)
        if  userAdditionalInfo.exists():
            for i in userAdditionalInfo:
                getId = i.id
                i.delete()
                print("i.id : ", getId)
                userAdditionalInfo = UserAdditionalInfo(id=getId, fcmToken= fcmTokenValue, user_id= user.id)
                userAdditionalInfo.save()
        else:
            userAdditionalInfoDetails =  UserAdditionalInfo.objects.all()
            print("userAdditionalInfoDetails: ", userAdditionalInfoDetails)
            if len(userAdditionalInfoDetails) == 0:
                print("userAdditionalInfoDetails not exists --------------->")
                userAdditionalInfo = UserAdditionalInfo(id=1, fcmToken=fcmTokenValue, user_id=user.id)
                userAdditionalInfo.save()
            else:
                userAdditionalInfo = UserAdditionalInfo(id=userAdditionalInfoDetails.reverse()[0].id + 1, fcmToken=fcmTokenValue, user_id=user.id)
                userAdditionalInfo.save()

        Token.objects.filter(user=user).delete()
        token, created = Token.objects.get_or_create(user=user)

        userData = {'id': user.id, 'first_name': user.first_name,'last_name': user.last_name, 'email': user.email, 'username': user.username}
        userTotalNotification = weather_ackno.objects.all()
        city = City.objects.filter(user_id= user.id)
        if city.exists():
            for i in city:
                return Response({'responseCode': 0, 'responseMessage': 'Success', 'userToken': token.key, 'userData': userData, 'city': i.town, 'userTotalNotification': len(userTotalNotification)})

        return Response({'responseCode': 0, 'responseMessage': 'Success', 'userToken': token.key, 'userData': userData, 'userTotalNotification': len(userTotalNotification)})