"""SmartEListApiProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from selApp import views
from selApp.auth import CustomAuthToken


urlpatterns = [
    path('admin/', admin.site.urls),
    path('requestOtp/', views.mobileRegisterApi),
    path('register/', views.registerApi),
    path('register/<int:id>', views.registerApi),
    path('login/', CustomAuthToken.as_view()),
    path('personInfo', views.getPersonalDetailApi),
    path('getHomeDetails/', views.getHomeDetailApi),
    path('scheduleItem/', views.scheduleListItems),
    path('scheduleItem/<int:id>', views.scheduleListItems),
    path('logout/', views.logout),
    path('updatecity/', views.updateCity),
    path('notification/', views.notification),
    path('search/', views.search_items_place),
    path('expiredScheduleItem/', views.expiredScheduleListItems),
    path('stateList/', views.StateList),
    path('cityList/', views.CityList),
    path('dateRangeScheduleList/', views.dateRangeScheduleList),
    path('cityS/', views.createCity),
    path('city/', views.createCitySub2)

]
