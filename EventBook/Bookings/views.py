from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import EventAdd,EventBook,Budget
from Accounts.models import Profile,Role
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime
from django.utils.timezone import make_aware



def home_view(request):
    events=EventAdd.objects.all().order_by("-start_at")
    authenticate=request.user.is_authenticated
    if request.user.is_authenticated:
        role=Role.objects.get(user=request.user)
        return render(request,"Attendee/attendeeHomePage.html",{"events":events,"user":request.user,"total":len(events),"choice":role.choice})
    return render(request,"Attendee/attendeeHomePage.html",{"events":events,"user":request.user,"total":len(events),"authenticate":authenticate})


def role_view(request):
    if request.method=="POST":
        choice=request.POST.get("choice")
        return render(request,"Accounts/login.html",{"choice":choice})
    return render(request,"Role/roleChoicesPage.html")



@login_required
def attendeeProfile_view(request):
    user=User.objects.get(username=request.user)
    profile=Profile.objects.get(user=user)
    booked=EventBook.objects.filter(user=user).order_by("-booked_at")
    role=Role.objects.get(user=user)
    return render(request,"Attendee/attendeeProfilePage.html",{"user":user,"profile":profile,"id":role.id,"choice":role.choice,"totalBooked":len(booked),"booked":booked})



@login_required
def organiserProfile_view(request):
    user=User.objects.get(username=request.user)
    profile=Profile.objects.get(user=user)
    events=EventAdd.objects.filter(user=user).order_by("start_at")
    role=Role.objects.get(user=user)
    registered=[]
    for i in events:
        registered.append(Budget.objects.get(event=i))
    attendees=0
    revnue=0.0
    for i in registered:
        attendees += i.persons
        revnue += i.amount
        
    return render(request,"Organiser/organiserProfile.html",{"user":user,"profile":profile,"id":role.id,"choice":role.choice,"attendees":attendees,"revnue":revnue,"totalEvents":len(events),"events":zip(events,registered)})





@login_required
def eventAdd_view(request,id):
    user=User.objects.get(id=id)
    role=Role.objects.get(user=user)
    if request.method=="POST":
        event_name=request.POST.get("eventName")
        descp=request.POST.get("eventDesp")
        event_category=request.POST.get("eventCategory")
        location=request.POST.get("location")
        venue=request.POST.get("venue")
        start_at=request.POST.get("startDateTime")
        end_at=request.POST.get("endDateTime")
        price=request.POST.get("price")
        tickets_avail=request.POST.get("ticketsAvailable")
        
        start_at=datetime.strptime(start_at,"%Y-%m-%dT%H:%M")
        end_at=datetime.strptime(end_at, "%Y-%m-%dT%H:%M")
        start_at = make_aware(start_at)
        end_at = make_aware(end_at)
        existing_event=EventAdd.objects.filter(location=location,venue=venue)
        for event in existing_event:
            if end_at > event.start_at and start_at < event.end_at:
                categories = EventAdd._meta.get_field("event_category").choices
                messages.warning(request,"This venue is already booked for the selected time.")
                return render(request,"Organiser/organiserEventAddPage.html",{"user":user,"categories":categories,"choice":role.choice})
                
        if start_at  > end_at:
            messages.warning(request,"Enter correct start and end dateTime")
            categories = EventAdd._meta.get_field("event_category").choices
            return render(request,"Organiser/organiserEventAddPage.html",{"user":user,"categories":categories,"choice":role.choice})
        
        event=EventAdd.objects.create(user=user,event_name=event_name,descp=descp,event_category=event_category,location=location,venue=venue,start_at=start_at,end_at=end_at,price=price,tickets_avail=tickets_avail,total_tickets=tickets_avail)
        budget=Budget.objects.create(event=event)
        messages.success(request,"Event addded successfully")
        return redirect("organiserProfile")
    
    categories = EventAdd._meta.get_field("event_category").choices
    return render(request,"Organiser/organiserEventAddPage.html",{"user":user,"categories":categories,"choice":role.choice})
    

def showEvent_view(request,id):
    event=EventAdd.objects.get(id=id)
    authenticate=request.user.is_authenticated
    if request.user.is_authenticated:
        role=Role.objects.get(user=request.user)
        return render(request,"Attendee/attendeeEventBookPage.html",{"event":event,"user":request.user,"choice":role.choice})
    return render(request,"Attendee/attendeeEventBookPage.html",{"event":event,"user":request.user,"authenticate":authenticate})


def showDetails_view(request,id):
    event=EventAdd.objects.get(id=id)
    authenticate=request.user.is_authenticated
    if request.user.is_authenticated:
        role=Role.objects.get(user=request.user)
        return render(request,"Attendee/attendeeEventDetailsPage.html",{"event":event,"user":request.user,"choice":role.choice})
    return render(request,"Attendee/attendeeEventDetailsPage.html",{"event":event,"user":request.user,"authenticate":authenticate})


def eventBook_view(request,id):
    if request.method=="POST":
        tickets=int(request.POST.get("tickets"))
        username=request.POST.get("username")
        password=request.POST.get("password")
        terms=request.POST.get("terms")=="on" 
        event=EventAdd.objects.get(id=id)
        budget=Budget.objects.get(event=event)
        print(budget.persons+tickets," ",event.total_tickets)
        if (budget.persons+tickets) > event.total_tickets:
              messages.error(request,"Tickets limit exceed")
              return redirect("home")
        
        if event.start_at < timezone.now() and event.end_at < timezone.now():
            messages.error(request,"Event already passed")
            event.is_active=False
            event.save()
            return redirect("home")

        if (budget.persons+tickets)==event.total_tickets:
            event.is_active=False
            event.save()

        user=authenticate(request,username=username,password=password)
        if not request.user.is_authenticated:
            messages.error(request,"Login required")
            return render(request,"Accounts/login.html",{"choice":"attendee"})
        if user is None:
            messages.error(request,"Username not exists")
            return render(request,"Accounts/signUp.html",{"choice":"attendee"})
        role=Role.objects.get(user=user)
        if role.check=="organiser":
            messages.warning(request,"Organiser can't book tickets")
            return render(request,"Attendee/attendeEventBookPage.html",{"event":event,"user":request.user})
        else:
            eventBook=EventBook.objects.create(user=user,event=event,tickets=tickets,amount=(event.price*tickets),terms=terms)
            event.tickets_avail=event.tickets_avail-tickets
            event.save()
            budget.amount=budget.amount + (event.price*tickets)
            budget.persons=budget.persons + tickets
            budget.save()
            messages.success(request,"Event booked successfully")
            return redirect("home")
    event=EventAdd.objects.get(id=id)
    return render(request,"Attendee/attendeEventBookPage.html",{"event":event,"user":request.user})



def cancelEvent_view(request,id):
    booked=EventBook.objects.get(id=id)
    event=EventAdd.objects.get(id=booked.event.id)
    now=timezone.now()
    diff=now - booked.booked_at
    if diff.seconds > 24*3600:
        messages.error(request,"Event can't be cancelled after 24 hours of booking")
        return redirect("attendeeProfile")
    budget=Budget.objects.get(event=booked.event)
    print("bef",budget.persons,budget.amount)
    budget.persons=budget.persons-booked.tickets
    budget.amount=budget.amount-booked.amount
    budget.save()
    event.tickets_avail = event.tickets_avail + booked.tickets
    event.is_active=True
    event.save()
    print("af",budget.persons,budget.amount)
    booked.delete()
    messages.success(request,"Event cancelled successfully")
    return redirect("attendeeProfile")

