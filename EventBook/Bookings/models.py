from django.db import models
from django.contrib.auth.models import User
from Accounts.models import Role
from django.utils import timezone


class EventAdd(models.Model):
    
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="eventAdd")
    event_name=models.TextField(null=False,blank=False)
    descp=models.TextField(null=True,blank=True)
    total_tickets=models.IntegerField(default=0,null=False,blank=False)
    tickets_avail=models.IntegerField(default=0,null=False,blank=False)
    price=models.FloatField(default=0.0,null=False,blank=False)
    location=models.TextField(null=False,blank=False)
    venue=models.TextField(null=False,blank=False)
    start_at=models.DateTimeField(null=False,blank=False)
    end_at=models.DateTimeField(null=False,blank=False)
    is_active=models.BooleanField(default=True)
    event_category=models.TextField(
        choices={ 
        ("Wedding", "Wedding"),
        ("Birthday", "Birthday"),
        ("Corporate Event", "Corporate Event"),
        ("Conference", "Conference"),
        ("Concert", "Concert"),
        ("Festival", "Festival"),
        ("Sports Event", "Sports Event"),
        ("Meetup", "Meetup"),
        ("Private Party", "Private Party"),
        ("Exhibition", "Exhibition"),
        ("Graduation", "Graduation"),
        ("Anniversary", "Anniversary"),
        ("Charity Event", "Charity Event"),
        ("Fashion Show", "Fashion Show"),
        ("Workshop", "Workshop"),
        ("Seminar", "Seminar"),
        ("Webinar", "Webinar"),
        ("Reunion", "Reunion"),
        ("Film Screening", "Film Screening"),
        ("Cultural Event", "Cultural Event"),
        ("Other", "Other"),
        }
        )
    


    def __str__(self):
        return f"{self.event_name}"
    


class Budget(models.Model):
    event=models.ForeignKey(EventAdd,on_delete=models.CASCADE,related_name="budget")
    persons=models.IntegerField(default=0)
    amount=models.FloatField(default=0.0)



class EventBook(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="eventBook")
    event=models.ForeignKey(EventAdd,on_delete=models.CASCADE)
    tickets=models.IntegerField(null=False,blank=False)
    amount=models.FloatField(null=False,blank=False)
    booked_at=models.DateTimeField(auto_now_add=True)
    terms=models.BooleanField(default=False,null=True,blank=True)
