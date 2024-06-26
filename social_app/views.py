from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from social_app.models import *
from django.contrib.auth import logout


def login(request):
    return render(request,"credential/login.html")

@login_required
def user_logout(request):
    logout(request)
    return redirect("login")

@login_required
def home(request):
    posts =ImagePost.objects.all()
    img_posts =TextPost.objects.all()
    profiles =Profile.objects.all()
    user_profile = Profile.objects.filter(user=request.user)
    if len(user_profile)>0:
        return render(request,"social_app/home.html" ,{"posts":posts, "img_posts":img_posts ,"profiles":profiles})
    return redirect("create_profile")

@login_required
def create_profile(request):
    if request.method == "POST":
        username = request.POST.get("username")
        profile_picture = request.FILES.get('pic')
        email= request.POST.get("email")
        date_of_birth =request.POST.get("dob")
        gender =request.POST.get("gender")
        about= request.POST.get("about")
        bio = request.POST.get("bio")
        print(username,email,date_of_birth,gender,about,bio)
        Profile.objects.create(user=request.user,username=username,bio=bio,email=email,date_of_birth=date_of_birth,gender=gender,about=about ,profile_picture=profile_picture )
        return redirect("home")
    user_profile=Profile.objects.filter(user=request.user)
    if len(user_profile)>0:
        return redirect("home")
    return render(request, 'profile/create_profile1.html')

@login_required
def view_profile(request,id):
    
    if id == 0:
        profile_info = Profile.objects.get(user=request.user)
        user_posts =ImagePost.objects.filter(user=request.user)
        img_posts= TextPost.objects.filter(user=request.user)
        count=user_posts.count() + img_posts.count()
        return render(request, 'profile/view_profile.html',{"profile_info":profile_info ,"posts":user_posts, "img_posts": img_posts, "count":count})
    
    profile_info =  Profile.objects.get(pk=id)
    user_posts =ImagePost.objects.filter(user=profile_info.user)
    img_posts =TextPost.objects.filter(user=profile_info.user)
    count=user_posts.count() + img_posts.count()
    return render(request, 'profile/view_profile.html',{"profile_info":profile_info ,"posts":user_posts, "img_posts":img_posts, "count":count})

@login_required
def delete_profile(request):
    profile_info = Profile.objects.get(user=request.user)
    for profile in Profile.objects.all():
        profile.followers.remove(request.user)
    profile_info.delete()
    text_posts = TextPost.objects.filter(user=request.user).delete()
    img_posts = ImagePost.objects.filter(user=request.user).delete()
    return redirect("create_profile")

@login_required
def edit_profile(request):
    if request.method == "POST" :
        profile_info = Profile.objects.get(user=request.user)
        profile_pic =profile_info.profile_picture
        profile_info.delete()
        username = request.POST.get("username")
        try:
            profile_picture = request.FILES.get('pic')
        except Exception as e:
            profile_picture = profile_pic
            print(e)
        email= request.POST.get("email")
        date_of_birth =request.POST.get("dob")
        gender =request.POST.get("gender")
        about= request.POST.get("about")
        bio = request.POST.get("bio")
        print(username,email,date_of_birth,gender,about,bio)
        profile_info =Profile.objects.create(user=request.user,username=username,bio=bio,email=email,date_of_birth=date_of_birth,gender=gender,about=about,profile_picture=profile_picture)
        
        return render(request, 'profile/view_profile.html',{"profile_info":profile_info})
    try: 
        profile_info = Profile.objects.get(user=request.user)
        return render(request, "profile/edit_profile1.html",{"profile_info":profile_info})
    except:
        return redirect("create_profile")

@login_required
def message(request):
    user = Profile.objects.get(user=request.user)
    print(user)
    print(user.following.all())
    friends = []   
    try:
        for i in user.following.all():
            friend= {}
            print(i.username)
            username = Profile.objects.get(user=i).username
            email = Profile.objects.get(user=i).email
            friend['username']=username
            friend['email']=email
            friends.append(friend)
    except:
        pass   
    print(friends)
    return render(request, 'chat/messaging.html' ,{"friends" : friends })

@login_required
def chat(request, request_username):
    user = Profile.objects.get(user=request.user)
    print(user)
    print(user.following.all())
    friends = []   
    try:
        for i in user.following.all():
            friend= {}
            print(i.username)
            username = Profile.objects.get(user=i).username
            email = Profile.objects.get(user=i).email
            friend['username']=username
            friend['email']=email
            friends.append(friend)
    except:
        pass   
    print(friends)
    
    profile = Profile.objects.get(username = request_username)
    from_user =request.user
    to_user= profile.user
    from django.db.models import Q
    if request.method =="POST":
        message_text = request.POST.get("message")
        Message.objects.create(from_user=from_user,to_user=to_user,message_text=message_text)
        messages = Message.objects.filter(Q(from_user=from_user,to_user=to_user) | Q(from_user=to_user, to_user=from_user))
        messages = messages.order_by('created_at')
        print(friends)
        return render(request, 'chat/chat_context.html' ,{"messages": messages,"friends" : friends ,"profile" :Profile.objects.all() ,"request_username": request_username})

    messages = Message.objects.filter(Q(from_user=from_user,to_user=to_user) | Q(from_user=to_user, to_user=from_user))
    messages = messages.order_by('created_at')
    print(friends)
    

    return render(request, 'chat/chat_context.html' ,{"messages": messages,"friends" : friends ,"profile" :Profile.objects.all() ,"request_username": request_username})


@login_required
def search_user(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, 'users/users.html',{"profiles":profiles})

@login_required
def follow(request,id):
    profile= Profile.objects.get(pk=id)
    profile.followers.add(request.user)
    
    profile_user= Profile.objects.get(user=request.user)
    profile_user.following.add(profile.user)
    
    profile.save()
    profile_user.save() 
    
    return redirect("search_user")

@login_required
def unfollow(request,id):
    profile= Profile.objects.get(pk=id)
    profile.followers.remove(request.user)
    
    profile_user= Profile.objects.get(user=request.user)
    profile_user.following.remove(profile.user)
    
    profile.save()
    profile_user.save()
    
    return redirect("search_user")


def create_post(request):
    if request.method == "POST" :
        if 'image' in request.POST :
            image = request.FILES.get('image')
            post_description = request.POST.get("description")
            hashtag = request.POST.get("hashtag")
            ImagePost.objects.create(user=request.user,post_picture=image,post_description=post_description,hashtag=hashtag)
            return redirect("home")
        
        elif 'text' in request.POST :
            post_description = request.POST.get("description")
            hashtag = request.POST.get("hashtag")
            TextPost.objects.create(user=request.user,post_description=post_description,hashtag=hashtag)
            return redirect("home")
        
    return render(request,"post/create_post.html")

def image_likes(request,id):
    img= ImagePost.objects.get(id=id)
    img.likes.add(request.user)
    img.save()
    return redirect('home')

def text_likes(request,id):
    text= TextPost.objects.get(id=id)
    text.likes.add(request.user)
    text.save()
    return redirect('home')