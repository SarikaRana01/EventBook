
from django.urls import path 
from .views import *

urlpatterns=[
    path("signUp/<str:choice>/",signUp_view,name="signUp"),
    path("login/<str:choice>/",login_view,name="login"),
    path("logout/<str:choice>/",logout_view,name="logout"),
    path("updatePhone/",updatePhone_view,name="updatePhone"),
    path("updateAddress/",updateAddress_view,name="updateAddress"),
    path("uploadImage/",uploadImage_view,name="uploadImage"),
    path("signUpGuest/",signUpGuest_view,name="signUpGuest")
]