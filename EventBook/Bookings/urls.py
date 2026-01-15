
from django.urls import path 
from .views import *

urlpatterns=[
    path("home/",home_view,name="home"),
    path("eventAdd/<int:id>",eventAdd_view,name="eventAdd"),
    path("eventBook/<int:id>",eventBook_view,name="eventBook"),
    path("",role_view,name="role"),
    path("eventAdd",eventAdd_view,name="eventAdd"),
    path("showEvent/<int:id>/",showEvent_view,name="showEvent"),
    path("showDetails/<int:id>/",showDetails_view,name="showDetails"),
    path("organiserProfile",organiserProfile_view,name="organiserProfile"),
    path("attendeeProfile/",attendeeProfile_view,name="attendeeProfile"),
    path("cancelEvent/<int:id>/",cancelEvent_view,name="cancelEvent"),
]