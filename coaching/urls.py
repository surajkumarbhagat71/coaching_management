from django.urls import path
from .views import *

urlpatterns = [
    path('',Home.as_view(),name="home"),
    path('usersingup',UserSignup.as_view(),name = 'usersignup'),
    path('adduserdetail',AddUserDetail.as_view(),name ="adduserdetail"),
    path('detailcourse/<int:pk>',DetailCourse.as_view(),name = 'detailcourse'),
    path('pandingrequest',PandingRequest.as_view(),name = 'pandingrequest'),
    path('login',Login.as_view(),name = "login"),
    path('logout',Logout.as_view(),name = "logout"),


    path('userjoincourse<int:pk>',UserJoinCourse.as_view(),name = 'userjoincourse'),
    path('paymentgenarate',PaymentGenarate.as_view(),name = 'paymentganarate'),

    #////////////////////////////////////// USER\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

    path('dashaboard',Dashaboard.as_view(),name = "dashaboard"),
    path('profile',Profile.as_view(),name = "profiel"),
    path('usercourse',UserCourse.as_view(),name ='usercourse'),
    path('payment',StudentPayment.as_view(),name = 'studentpayment'),
    path('requestpayment/<int:pk>',PaymentRequest.as_view(),name = 'paymentrequest'),
    path('studetupdateprofile/<int:pk>',StudentProfileUpdate.as_view(),name = "studentupdateprofile"),


    #///////////////////////////////////// ADMIN WORK \\\\\\\\\\\\\\\\\\\\\\\

    path('admindashaboard',AdminDashaboard.as_view(),name = 'admindashaboard'),
    path('addcourse',AddCourse.as_view(),name = 'addcourse'),
    path('requestforaddmision',RequestforAddmision.as_view(),name = 'requestforaddmision'),
    path('requestforcourse',Requestforcourse.as_view(),name = 'requestforcourse'),
    path('allstudent',AllStudent.as_view(),name = "allstudent"),
    path('apseptpayment/<int:pk>',ApseptPayment.as_view(),name = 'apseptpayment'),
    path('apseptadmission/<int:pk>',ApseptAdminssion.as_view(),name="apseptadmission"),
    path('apseptcourse/<int:pk>',ApseptCourse.as_view(),name="apseptcourse"),

]
