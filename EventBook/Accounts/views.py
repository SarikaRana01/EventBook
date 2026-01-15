
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from .models import Role
from django.contrib import messages
from Bookings.models import EventAdd,Budget
from Accounts.models import Profile
from django.contrib.auth.decorators import login_required



def signUp_view(request,choice):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        email=request.POST.get("email")
        user=authenticate(request,username=username,password=password)
        if user is not None:
            messages.error(request,"Username already exists!")
            return render(request,"Accounts/signUp.html",{"choice":choice})
        user=User.objects.create(username=username,email=email)
        Profile.objects.create(user=user)
        role=Role.objects.create(user=user,choice=choice)
        user.set_password(password)
        user.save()
        login(request,user)
        messages.success(request,"Successfully Logged In")
        if role.choice=="organiser":
            return redirect("organiserProfile")
        return redirect("home")
    return render(request,"Accounts/signUp.html",{"choice":choice})


def signUpGuest_view(request):
    return render(request,"Accounts/signUp.html",{"choice":"attendee"})

def login_view(request,choice):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=authenticate(request,username=username,password=password)
        if user is not None:
            role=Role.objects.get(user=user)
            login(request,user)
            messages.success(request,"Successfully Logged In")
            if role.choice=="organiser":
               return redirect("organiserProfile")
            return redirect("home") 
        else:
         messages.error(request,"Username not exists!") 
    return render(request,"Accounts/login.html",{"choice":choice})


@login_required
def logout_view(request,choice):
    logout(request)
    messages.success(request,"Successfully Logged Out")
    return render(request,"Accounts/login.html",{"choice":choice})
    



@login_required
def updatePhone_view(request):
    role=Role.objects.get(user=request.user)
    print(role)
    if request.method=="POST":
        phone=request.POST.get("phone")
        profile=Profile.objects.get(user=request.user)
        print(profile)
        profile.phone=phone
        profile.save()
        messages.success(request,"Phone number updated")
    if role.choice=="organiser":
        return redirect("organiserProfile")
    return redirect("attendeeProfile")



@login_required
def updateAddress_view(request):
    role=Role.objects.get(user=request.user)
    if request.method=="POST":
        address=request.POST.get("address")
        profile=Profile.objects.get(user=request.user)
        profile.address=address
        profile.save()
        messages.success(request,"Address updated")
    if role.choice=="organiser":
        return redirect("organiserProfile")
    return redirect("attendeeProfile")



@login_required
def uploadImage_view(request):
    role=Role.objects.get(user=request.user)
    if request.method=="POST":
        image=request.FILES.get("image")
        profile=Profile.objects.get(user=request.user)
        profile.image=image
        profile.save()
        messages.success(request,"Profile image updated")
    if role.choice=="organiser":
        return redirect("organiserProfile")
    return redirect("attendeeProfile")

    