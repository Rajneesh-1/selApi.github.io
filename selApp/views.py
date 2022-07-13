from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.utils import json
from .models import Home, ScheduleItemList, City, weather_ackno, ExpiredItemList, MobileRegistration, AuthToken, UserAdditionalInfo, PersonInfo, AvailableCity, TotalCity
from .serializers import UserSerializers, HomeSerializers, ScheduleItemListSerializers, CitySerializers, WeatherAcknoSerializers, ExpiredListSerializers, AuthTokenSerializer, PersonInfoSerializers, AvailableCitySerializers, TotalCitySerializers
from rest_framework import status
from datetime import datetime
import pytz
import urllib
from bs4 import BeautifulSoup
from os import path
import binascii, os

CURRENT_TOKEN_MODEL = AuthToken.objects #Token.objects
# Create your views here.


@api_view(['POST'])
def mobileRegisterApi(request):
    if request.method == 'POST':
        received_json_mobileNo = json.loads(request.body.decode("utf-8"))['mobileNo']
        try:
            received_json_otp = json.loads(request.body.decode("utf-8"))['otp']
        except:
            received_json_otp =""
        current_local_time = datetime.now(pytz.timezone('Asia/Kolkata'))
        if "+91" in received_json_mobileNo:
            mobileNo = received_json_mobileNo.split("+91")
            if(len(mobileNo[1]) == 10):
                if (MobileRegistration.objects.filter(mobileNo = received_json_mobileNo).exists()):
                    getMobileRegData = MobileRegistration.objects.get(mobileNo = received_json_mobileNo)
                    if received_json_otp and received_json_otp.isdigit() and len(received_json_otp) == 4:
                        if getMobileRegData.otp == received_json_otp:
                            current_date_time_object = datetime.strptime(current_local_time.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                            scheduled_datetime_object = datetime.strptime(getMobileRegData.otptimeStamp.split(".")[0], '%Y-%m-%d %H:%M:%S')

                            print("remainingTime: ", (current_date_time_object - scheduled_datetime_object).total_seconds())
                            if ((current_date_time_object - scheduled_datetime_object).total_seconds() > 300):
                                return Response({'responseCode': 114, 'responseMessage': "Invalid Otp"})
                            else:
                                MobileRegistration.objects.filter(mobileNo=received_json_mobileNo).update(otptimeStamp = "", otp= "")

                                try:
                                    city = City.objects.get(user_id=getMobileRegData.id).town
                                    notificationCount = len(weather_ackno.objects.filter(user_id = getMobileRegData.id))
                                except:
                                    city=None
                                    notificationCount = None

                                fcmTokenValue = request.META.get('HTTP_AUTHORIZATION', b'')
                                authTokenObjectList = AuthToken.objects.filter(user_id=getMobileRegData.id)
                                if authTokenObjectList.exists():
                                    print("---------------------------------------exists----------------------------------------")
                                    serializer = AuthTokenSerializer(authTokenObjectList[0], data={"key": binascii.hexlify(os.urandom(20)).decode(), "user": getMobileRegData.id})
                                    if serializer.is_valid():
                                        serializer.save()
                                        saveFcmToken(fcmTokenValue, getMobileRegData.id)
                                        return Response({'responseCode': 0, 'responseMessage': "Success", "responseData":[serializer.data], "city": city,"notificationCount":notificationCount, "mobileNo": received_json_mobileNo})
                                else:
                                    print("---------------------------------------not exists----------------------------------------")
                                    authTokenAllObjectList = AuthToken.objects.all()
                                    if len(authTokenAllObjectList) == 0:
                                        userAdditionalInfo = AuthToken(id=1, key= binascii.hexlify(os.urandom(20)).decode(), user_id= getMobileRegData.id)
                                        userAdditionalInfo.save()
                                        saveFcmToken(fcmTokenValue, getMobileRegData.id)
                                        serializer = AuthTokenSerializer(userAdditionalInfo)
                                        return Response({'responseCode': 0, 'responseMessage': "Success", "responseData":[serializer.data], "city": city,"notificationCount":notificationCount, "mobileNo": received_json_mobileNo})
                                    else:
                                        userAdditionalInfo = AuthToken(id=authTokenAllObjectList.reverse()[0].id + 1, key= binascii.hexlify(os.urandom(20)).decode(), user_id= getMobileRegData.id)
                                        userAdditionalInfo.save()
                                        saveFcmToken(fcmTokenValue, getMobileRegData.id)
                                        serializer = AuthTokenSerializer(userAdditionalInfo)
                                        print("serializer", serializer)
                                        return Response({'responseCode': 0, 'responseMessage': "Success", "responseData":[serializer.data], "city": city,"notificationCount":notificationCount, "mobileNo": received_json_mobileNo})
                                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                        return Response({'responseCode': 117, 'responseMessage': "Incorrect Otp"})

                    else:
                        import random
                        number = random.randint(1000,9999)
                        MobileRegistration.objects.filter(mobileNo=received_json_mobileNo).update(otptimeStamp = current_local_time, otp= number)
                        return Response({'responseCode': 0, 'responseMessage': "Success", "responseData": [{"otp": number}]})

                else:
                    import random
                    number = random.randint(1000,9999)
                    createMobileRegistration = MobileRegistration.objects.create(mobileNo=received_json_mobileNo, otptimeStamp= current_local_time, otp= number)
                    createMobileRegistration.save()
                    return Response({'responseCode': 0, 'responseMessage': "Success", "responseData": [{"otp": number}]})
            else:
                return Response({'responseCode': 114, 'responseMessage': "Invalid Mobile No."})
        return Response({'responseCode': 115, 'responseMessage': "Please Provide CountryCode"})

def saveFcmToken(fcmTokenValue, id):
    #---------Save Fcm Token ---------#

        print("fcmTokenValue:", fcmTokenValue)
        if (fcmTokenValue != None):
            userAdditionalInfo = UserAdditionalInfo.objects.filter(user_id=id)
            print("userAdditionalInfo: ",userAdditionalInfo)
            if  userAdditionalInfo.exists():
                for i in userAdditionalInfo:
                    getId = i.id
                    i.delete()
                    print("i.id : ", getId)
                    userAdditionalInfo = UserAdditionalInfo(id=getId, fcmToken= fcmTokenValue, user_id= id)
                    userAdditionalInfo.save()
            else:
                userAdditionalInfoDetails =  UserAdditionalInfo.objects.all()
                print("userAdditionalInfoDetails: ", userAdditionalInfoDetails)
                if len(userAdditionalInfoDetails) == 0:
                    print("userAdditionalInfoDetails not exists --------------->")
                    userAdditionalInfo = UserAdditionalInfo(id=1, fcmToken=fcmTokenValue, user_id=id)
                    userAdditionalInfo.save()
                else:
                    print("not exists --------------->")
                    userAdditionalInfo = UserAdditionalInfo(id=userAdditionalInfoDetails.reverse()[0].id + 1, fcmToken=fcmTokenValue, user_id=id)
                    userAdditionalInfo.save()

    #---------************** ---------#

@api_view(['GET', 'POST'])
def registerApi(request, id=None):
    if request.method == 'GET':
        id = id
        try:
            if id is not None:
                registerUserObject = User.objects.get(id=id)
                serializer = UserSerializers(registerUserObject)
                return Response({'responseCode': 0, 'responseMessage': "Success", 'responseData': serializer.data,
                                 'nativeCurrencyCode': "+91"})
        except:
            return Response({'responseCode': 101, 'responseMessage': "No Data exists"})

        if id is not None:
            registerUserObject = RegisterUser.objects.get(id=id)
            serializer = RegisterSerializers(registerUserObject)
            return Response({'responseCode': 0, 'responseMessage': "Success", 'responseData': serializer.data, 'nativeCurrencyCode': "+91"})

        registerUserAllObjects = RegisterUser.objects.all()
        serializer = RegisterSerializers(registerUserAllObjects, many=True)
        return Response({'responseCode':0, 'responseMessage': 'Success', 'responseData': serializer.data})

        registerUserAllObjects = User.objects.all()
        serializer = UserSerializers(registerUserAllObjects, many=True)
        return Response({'responseCode': 0, 'responseMessage': 'Success', 'responseData': serializer.data})

    if request.method == 'POST':
        serializer = UserSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(
                {'responseCode': 0, 'responseMessage': "You have registered Successfully"})
        return Response({'responseCode': 111, 'responseMessage': "Invalid Data"})

@api_view(['GET'])
def getHomeDetailApi(request):
    if request.method == "GET":
        homeObjects = Home.objects.all()
        if homeObjects.exists():
            homeSerializer = HomeSerializers(homeObjects, many=True)
            return Response({'responseCode': 0, 'responseMessage': "Success", 'responseData': homeSerializer.data})
        return Response({'responseCode': 101, 'errorMessage': "No Data Exists"})

@api_view(['GET'])
def getPersonalDetailApi(request):
    if request.method == "GET":
        personInfoObjects = PersonInfo.objects.all()
        if personInfoObjects.exists():
            personInfoObjectsSerializer = PersonInfoSerializers(personInfoObjects, many=True)
            return Response({'responseCode': 0, 'responseMessage': "Success", 'responseData': personInfoObjectsSerializer.data})
        return Response({'responseCode': 101, 'errorMessage': "No Data Exists"})



@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def scheduleListItems(request, id=None):
    if request.method == "GET":
        data = request.META.get('HTTP_AUTHORIZATION', b'')
        if (CURRENT_TOKEN_MODEL.filter(key=data).exists()) :
            id = CURRENT_TOKEN_MODEL.get(key=data).user
            registerUserScheduledObject = ScheduleItemList.objects.filter(user_id=id)
            if registerUserScheduledObject.exists():
                serializer = ScheduleItemListSerializers(registerUserScheduledObject, many=True)
                return Response({'responseCode': 0, 'responseMessage': "Success", 'responseData':serializer.data})
            else:
                return Response({'responseCode': 101, 'responseMessage': "No Data Exists"})
        else:
            print(CURRENT_TOKEN_MODEL.filter(user_id=id))
            return Response({'responseCode': 107, 'responseMessage': "Session Expired"})  #/////////////////////to be done ...pending

        scheduleListItems = ScheduleItemList.objects.all()
        serializer = ScheduleItemListSerializers(scheduleListItems, many=True)
        if scheduleListItems.exists():
            return Response({'responseCode': 0, 'responseMessage': "Success", 'responseData': serializer.data})
        return Response({'responseCode': 101, 'responseMessage': "No Data Exists"})

    if request.method == "POST":

        data = request.META.get('HTTP_AUTHORIZATION', b'')
        serializer = ScheduleItemListSerializers(data=request.data)
        if serializer.is_valid():
            tokenDataRow = CURRENT_TOKEN_MODEL.filter(key=data)
            if tokenDataRow.exists():
                for i in tokenDataRow:
                    city = City.objects.filter(user_id= i.user_id)
                    if city.exists():
                        for i in city:
                            serializer.save(user_id = i.user_id)
                            return Response({'responseCode': 0, 'responseMessage': "Your Scheduled Data Saved Successfully"})
                    else: return Response({'responseCode': 113, 'responseMessage': 'City not present!'})

            else:
                return Response({'responseCode': 107, 'responseMessage': "Session Expired"})

        else:
            return Response({'responseCode': 111, 'responseMessage': "Invalid Data"})

    if request.method == "PUT":
        data = request.META.get('HTTP_AUTHORIZATION', b'')
        user = CURRENT_TOKEN_MODEL.filter(key=data)
        if user.exists():
            for i in user:

                    userScheduledData = ScheduleItemList.objects.get(id = id)
                    serializer = ScheduleItemListSerializers(userScheduledData, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        scheduledListObjects = ScheduleItemList.objects.filter(user_id=i.user)
                        serializersScheduledListAllObjects = ScheduleItemListSerializers(scheduledListObjects, many= True)
                        return Response({'responseCode': 0, 'responseMessage': "Success", 'responseData': serializersScheduledListAllObjects.data})
                    else:
                        return Response({'responseCode': 111, 'responseMessage': "Invalid Data"})

        else:
            return Response({'responseCode': 107, 'responseMessage': "Session Expired"})

    if request.method == "DELETE":
        if id is not None:
            schedule_item_id = id
            data = request.META.get('HTTP_AUTHORIZATION', b'')
            matchToken = CURRENT_TOKEN_MODEL.filter(key=data)
            if matchToken.exists():
                    scheduleListItem = ScheduleItemList.objects.filter(id = schedule_item_id)
                    if scheduleListItem.exists():
                        ScheduleItemList.objects.get(id=schedule_item_id).delete()
                        return Response({'responseCode': 0, 'responseMessage': "Scheduled item deleted successfully.", "remainingItems": len(ScheduleItemList.objects.filter(id = schedule_item_id))})
                    else:
                        return Response({'responseCode': 102, 'responseMessage': "Invalid User Id"})
            else:
                return Response({'responseCode': 107, 'responseMessage': "Session Expired"})
        else:
            return Response({'responseCode': 112, 'responseMessage': "Please provide scheduled item id"})

@api_view(['POST'])
def logout(request):
    if request.method == 'POST':
        data = request.META.get('HTTP_AUTHORIZATION', b'')
        getUserId = CURRENT_TOKEN_MODEL.filter(key=data)
        if getUserId.exists():
            for i in getUserId:
                CURRENT_TOKEN_MODEL.filter(user=i.user_id).delete()
                return Response({"responseCode": 0, "responseMessage": "Successfully Logout"})
        else:
            return Response({"responseCode": 101, "responseMessage": "No Data Exists"})

@api_view(['PATCH', 'POST', 'GET'])
def updateCity(request):
    if request.method == 'PATCH':
        data = request.META.get("HTTP_AUTHORIZATION", b'')
        getUserId = CURRENT_TOKEN_MODEL.filter(key=data)

        if getUserId.exists():
            for i in getUserId:
                cityData = City.objects.filter(user_id=i.user_id)
            if cityData.exists():
                for city in cityData:
                    serializer = CitySerializers(city, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response({"responseCode": 0, "responseMessage": "City updated successfully", "data": serializer.data})
                    else:
                        return Response({"responseCode": 111, "responseMessage": "Invalid Data"})
            else:
                return Response({"responseCode": 101, "responseMessage": "No Data Exists"})
        else:
                return Response({'responseCode': 107, 'responseMessage': "Session Expired"})

    if request.method == 'POST':
            data = request.META.get("HTTP_AUTHORIZATION", b'')

            getUserId = CURRENT_TOKEN_MODEL.filter(key=data)
            if getUserId.exists():
                for i in getUserId:
                    if (City.objects.filter(user_id=i.user_id).exists()):
                        return Response({"responseCode": 106, "responseMessage": "City already available."})
                    else:
                        serializers = CitySerializers(data=request.data)
                        if serializers.is_valid():
                            serializers.save(user_id=i.user_id)
                            return Response({"responseCode": 0, "responseMessage": "City added successfully", "data": [serializers.data]})
                        else:
                            return Response({"responseCode": 111, "responseMessage": "Invalid Data"})
            else:
                return Response({'responseCode': 107, 'responseMessage': "Session Expired"})


    if request.method == 'GET':
        cityDetails = City.objects.all()
        serializers = CitySerializers(cityDetails, many=True)
        return Response({"responseCode": 0, "responseMessage": "Success", "data": serializers.data})


@api_view(['GET'])
def notification(request, id=None):
    if request.method == "GET":
        if id is not None:
            data = request.META.get('HTTP_AUTHORIZATION', b'')
            if (CURRENT_TOKEN_MODEL.filter(key=data).exists()) :
                id = CURRENT_TOKEN_MODEL.get(key=data).user
                notificationObjects = weather_ackno.objects.filter(user_id=id)
                if notificationObjects.exists():
                    serializer = WeatherAcknoSerializers(notificationObjects, many=True)
                    return Response({'responseCode': 0, 'responseMessage': "Success", 'responseData':serializer.data})
                else:
                    return Response({'responseCode': 101, 'responseMessage': "No Data Exists"})
            else:
                return Response({'responseCode': 107, 'responseMessage': "Session Expired"})

        allNotificationItems = weather_ackno.objects.all()
        serializer = WeatherAcknoSerializers(allNotificationItems, many=True)
        if allNotificationItems.exists():
            return Response({'responseCode': 0, 'responseMessage': "Success", 'responseData': serializer.data})
        return Response({'responseCode': 101, 'responseMessage': "No Data Exists"})

@api_view(['POST'])
def search_items_place(request):
    if request.method == "POST":
        data = request.META.get("HTTP_AUTHORIZATION", b'')
        newData = []

        if (CURRENT_TOKEN_MODEL.filter(key=data).exists()):
            received_json_searchItem = json.loads(request.body.decode("utf-8"))['searchItem']
            received_json_localPlace = json.loads(request.body.decode("utf-8"))['localPlace']
            received_json_city = json.loads(request.body.decode("utf-8"))['city']
            print("111111111111111111111111111111111111111111111111")
            try:
                searchItem = ''
                for i in received_json_searchItem.split(" "):
                    searchItem = searchItem + i     # If 2 or more than 2 words for search Item is given

                localPlace = ''
                for i in received_json_localPlace.split(" "):
                    localPlace = localPlace + i     # If 2 or more than 2 words for local place is given

                if " " not in received_json_city:   # If city not given
                    url = 'https://www.google.com/search?safe=strict&rlz=1C1PRFI_enIN903IN903&biw=1017&bih=730&tbm=lcl&ei=LJuNX-XVKpOC4-EPgbuY-Ag&q=' + 'list' + 'of' + searchItem + 'in' + localPlace + received_json_city

                else:                               # If city given
                    city = ''
                    for i in received_json_city.split(" "):
                        city = city + i
                    url = 'https://www.google.com/search?safe=strict&rlz=1C1PRFI_enIN903IN903&biw=1017&bih=730&tbm=lcl&ei=LJuNX-XVKpOC4-EPgbuY-Ag&q=' + 'list' + 'of' + searchItem + 'in' + localPlace + city

                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'})
                web_byte = urllib.request.urlopen(req).read()
                webpage = web_byte.decode('utf-8')

                page_soup = BeautifulSoup(webpage, 'html.parser')
                containers = page_soup.find_all('div', attrs={'class': 'VkpGBb'})
                c = 0
                list = []

                for container in containers:
                    try:
                        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
                        #shop_name = container.findAll('div', {'class': 'cXedhc uQ4NLd'})
                        shop_name = container.findAll('div', {'class': 'cXedhc'})
                        list.append([])
                        # Logic for Shop Name
                        #XX = shop_name[0].find('div', {'class': 'dbg0pd'})
                        XX = shop_name[0].find('div',{'class':'dbg0pd OSrXXb eDIkBe'})
                        print("shop_name[0]", shop_name[0])

                        print("XX.stripped_strings", XX.stripped_strings)
                        for i in XX.stripped_strings:
                            print(i)

                        for i in XX.stripped_strings:
                            list[c].append(i)
                        print("|1|"*30)
                        # Logic for Other details of Shop
                        YY = shop_name[0].find('div', {'class': 'rllt__details'})
                        for i in YY.stripped_strings:
                         print(i)

                        type = shop_name[0].find('span', {'class': 'z3HNkc'})
                        print("-"*30)
                        print(type)
                        print("-"*30)
                        # print("  Type shop_name[0].findAll(('div',{'class':'rllt__details lqhpac'})):",type(shop_name[0].find('span',{'class':'rllt__details lqhpac'})))
                        for i in YY.stripped_strings:
                         list[c].append(i)
                        c = c + 1

                        mist=[]
                        for i in list:
                            if len(i)!=0:
                                mist.append(i)

                        for data in mist:
                            tempData = dict()
                        for i in range(len(data)):
                            if (i == 0):
                                tempData["title"] = data[i]
                            if (i == 1):
                                tempData["subTitle"] = data[i]
                            if ("." in data[i]):
                                tempData["rating"] = data[i]
                            if ("(" in data[i] and len(data[i]) < 5):
                                tempData["noOfPeoples"] = data[i]
                            #if ("·" in data[i]):
                            #    tempData["type"] = data[i]
                            if ("," in data[i]):
                                tempData["address"] = data[i]
                            if ("close" in data[i].lower() or "open" in data[i].lower()):
                                tempData["timing"] = data[i]

                        newData.append(tempData)
                        #list(set(newData))

                    except:
                        shop_name = container.findAll('div', {'class': 'cXedhc'})
                        list.append([])
                        # Logic for Shop Name
                        #XX = shop_name[0].find('div', {'class': 'dbg0pd'})
                        XX = shop_name[0].find('div',{'class':'dbg0pd eDIkBe'})
                        print("XX: ",XX)
                        for i in XX.stripped_strings:
                            list[c].append(i)

                        # Logic for Other details of Shop
                        #YY = shop_name[0].find('span', {'class': 'rllt__details lqhpac'})
                        YY = shop_name[0].find('div', {'class': 'rllt__details'})
                        print("YY", YY)
                        # print("  Type shop_name[0].findAll(('div',{'class':'rllt__details lqhpac'})):",type(shop_name[0].find('span',{'class':'rllt__details lqhpac'})))
                        for i in YY.stripped_strings:
                            list[c].append(i)

                        c = c + 1

                        mist=[]
                        for i in list:
                            if len(i)!=0:
                                mist.append(i)
                        for data in mist:
                            tempData = dict()
                            for i in range(len(data)):
                                if (i == 0):
                                    tempData["title"] = data[i]
                                if (i == 1):
                                    tempData["subTitle"] = data[i]
                                if ("." in data[i]):
                                    tempData["rating"] = data[i]
                                if ("(" in data[i] and len(data[i]) < 5):
                                    tempData["noOfPeoples"] = data[i]
                                #if ("·" in data[i]):
                                #    tempData["type"] = data[i]
                                if ("," in data[i]):
                                    tempData["address"] = data[i]
                                if ("close" in data[i].lower() or "open" in data[i].lower()):
                                    tempData["timing"] = data[i]
                            newData.append(tempData)
                        #list(set(newData))


                print("list : ",list)
                print("len list : ",len(list))


                print("mist: ",mist)
                print("newData: ",newData)

                if len(mist)==0:
                    Response({'responseCode': 0, 'responseMessage': "Success", 'responseData': [], 'listLen': len(newData)})

                return Response({'responseCode': 0, 'responseMessage': "Success", 'responseData': newData})

            except:
                Response({'responseCode': 0, 'responseMessage': "Success", 'responseData': [], 'listLen': len(newData)})
            #return render(request, 'enroll/scrape.html',{'sm':sm,'city':city.city_name,'list':mist,'l':l,'search':search})
        else:
            return Response({'responseCode': 107, 'responseMessage': "Session Expired"})


@api_view(['GET'])
def expiredScheduleListItems(request):
    if request.method == "GET":
        data = request.META.get('HTTP_AUTHORIZATION', b'')
        if (CURRENT_TOKEN_MODEL.filter(key=data).exists()) :
            id = CURRENT_TOKEN_MODEL.get(key=data).user
            expiredScheduledObject = ExpiredItemList.objects.filter(user_id=id)
            if expiredScheduledObject.exists():
                serializer = ExpiredListSerializers(expiredScheduledObject, many=True)
                return Response({'responseCode': 0, 'responseMessage': "Success", 'responseData':serializer.data})
            else:
                return Response({'responseCode': 101, 'responseMessage': "No Data Exists"})
        else:
            return Response({'responseCode': 107, 'responseMessage': "Session Expired"})

@api_view(['GET'])
def StateList(requesst):
        ROOT=path.dirname(path.realpath(__file__))
        print("ROOT",ROOT)
        excelFilePath = path.join(ROOT,'Town_Codes_2001.xls')
        print("excelFilePath", excelFilePath)

        df = pd.DataFrame(pd.read_excel(excelFilePath))
        newData = df.iloc[1:, 0:]
        stateList = sorted(list(set(newData["State/Union"])))

        return Response({"responseCode": 0, "responseMessage": "Success", "data": stateList})


@api_view(['POST'])
def CityList(request):
    if request.method == "POST":
        ROOT=path.dirname(path.realpath(__file__))
        print("ROOT",ROOT)
        excelFilePath = path.join(ROOT,'Town_Codes_2001.xls')
        df = pd.DataFrame(pd.read_excel(excelFilePath))
        newData = df.iloc[1:, 0:]
        stateName = request.data
        print("========>",stateName)
        cityList = list(newData.loc[newData["State/Union"] == stateName["state"]]['City/Town'])

        return Response({"responseCode": 0, "responseMessage": "Success", "data": cityList})
    else:
        return Response({"responseCode": 104, "responseMessage": "Something went wrong !"})

@api_view(['POST'])
def dateRangeScheduleList(request,id=None):
    if request.method == "POST":
        fromDate    = json.loads(request.body.decode("utf-8"))['fromDate']
        toDate      = json.loads(request.body.decode("utf-8"))['toDate']
        data = request.META.get('HTTP_AUTHORIZATION', b'')
        if (CURRENT_TOKEN_MODEL.filter(key=data).exists()):
            try:
                id = CURRENT_TOKEN_MODEL.get(key=data).user
                scheduledListObjects = ScheduleItemList.objects.filter(user_id=id)
                scheduledListObjectsSerializer = ScheduleItemListSerializers(scheduledListObjects, many=True)

                dateRangeFilteredListObjects = ScheduleItemList.objects.filter(date__range=(fromDate, toDate)).filter(user_id=id)
                dateRangeFilteredListObjectsSerializer = ScheduleItemListSerializers(dateRangeFilteredListObjects, many=True)

                return Response({"responseCode": 0, "responseMessage": "Success", "responseData": [{"upcomingScheduledData": dateRangeFilteredListObjectsSerializer.data, "allScheduledListData": scheduledListObjectsSerializer.data}]})

            except:

                return Response({'responseCode': 111, 'responseMessage': "Invalid Data"})
        else:
            return Response({'responseCode': 107, 'responseMessage': "Session Expired"})
        return Response({'responseCode': 102, 'responseMessage': "Invalid User Id"})


@api_view(['GET', 'POST'])
def createCity(request):
    if request.method == "POST":
        availableCity = json.loads(request.body.decode("utf-8"))['availableCity']
        for i in availableCity["city"]:
            if AvailableCity.objects.filter(availableCity=i).exists():
                return Response({'responseCode':105, 'responseMessage': 'City already available.'})

            AvailableCity.objects.create(availableCity=i)

        availableCityAllObjects = AvailableCity.objects.all()
        serializer = AvailableCitySerializers(availableCityAllObjects, many=True)
        return Response({'responseCode':0, 'responseMessage': 'Success', 'responseData': serializer.data})
    else:
        availableCityAllObjects = AvailableCity.objects.all()
        serializer = AvailableCitySerializers(availableCityAllObjects, many=True)
        return Response({'responseCode':0, 'responseMessage': 'Success', 'responseData': serializer.data})

@api_view(['GET', 'POST'])
def createCitySub2(request):
    if request.method == "POST":
        allTotalCity = json.loads(request.body.decode("utf-8"))['availableCity']
        """for i in allTotalCity["city"]:
            if TotalCity.objects.filter(totalCity=i).exists():
                return Response({'responseCode':105, 'responseMessage': 'City already available.'})"""

        TotalCity.objects.create(totalCity=allTotalCity["city"])

        totalCityAllObjects = TotalCity.objects.all()
        serializer = TotalCitySerializers(totalCityAllObjects, many=True)
        print(serializer.data)
        return Response({'responseCode':0, 'responseMessage': 'Success', 'responseData': serializer.data})
    else:
        totalCityAllObjects = TotalCity.objects.all()
        serializer = TotalCitySerializers(totalCityAllObjects, many=True)
        print("-"*100)
        print(type(serializer.data))
        print(type(serializer.data[0]))
        print()
        lis = list(serializer.data[0].values())

        return Response({'responseCode':0, 'responseMessage': 'Success', 'responseData': eval(lis[0])})
