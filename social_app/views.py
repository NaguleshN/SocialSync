from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from social_app.models import *
from django.contrib.auth import logout

# Create your views here.
def login(request):
    return render(request,"credential/login.html")

@login_required
def user_logout(request):
    logout(request)
    return redirect("login")

@login_required
def home(request):
    user_profile = Profile.objects.filter(user=request.user)
    if len(user_profile)>0:
        return render(request,"social_app/home.html")
    return redirect("create_profile")

@login_required
def create_profile(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email= request.POST.get("email")
        date_of_birth =request.POST.get("dob")
        gender =request.POST.get("gender")
        about= request.POST.get("about")
        bio = request.POST.get("bio")
        print(username,email,date_of_birth,gender,about,bio)
        Profile.objects.create(user=request.user,username=username,bio=bio,email=email,date_of_birth=date_of_birth,gender=gender,about=about )
        return redirect("home")
    user_profile=Profile.objects.filter(user=request.user)
    if len(user_profile)>0:
        return redirect("home")
    return render(request, 'profile/create_profile.html')

@login_required
def view_profile(request):
    profile_info = Profile.objects.get(user=request.user)
    print(profile_info)
    return render(request, 'profile/view_profile.html',{"profile_info":profile_info})

@login_required
def delete_profile(request):
    profile_info = Profile.objects.get(user=request.user)
    profile_info.delete()
    return redirect("create_profile")

@login_required
def edit_profile(request):
    if request.method == "POST" :
        profile_info = Profile.objects.get(user=request.user)
        profile_info.delete()
        username = request.POST.get("username")
        email= request.POST.get("email")
        date_of_birth =request.POST.get("dob")
        gender =request.POST.get("gender")
        about= request.POST.get("about")
        bio = request.POST.get("bio")
        print(username,email,date_of_birth,gender,about,bio)
        Profile.objects.create(user=request.user,username=username,bio=bio,email=email,date_of_birth=date_of_birth,gender=gender,about=about )
        return redirect("view_profile")
    profile_info = Profile.objects.get(user=request.user)
    return render(request, "profile/edit_profile.html",{"profile_info":profile_info})

@login_required
def chat(request):
    return render(request, 'chat/messaging.html')
