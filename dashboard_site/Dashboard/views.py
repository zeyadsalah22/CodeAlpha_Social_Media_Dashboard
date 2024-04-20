from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User,SocialMediaAccount


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request,'Dashboard/login.html',{
                "message": 'Invalid username and/or password'
            })
    else:
        return render(request,'Dashboard/login.html')
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    if request.method=='POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmation = request.POST['confirmation']

        if password!=confirmation:
            return render(request,'Dashboard/register.html',{
                'message': "Passwords don't match"
            })
        try:
            user = User.objects.create_user(username,email,password)
            user.save()

        except IntegrityError:
            return render(request,'Dashboard/register.html',{
                'message': "Username already taken"
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "Dashboard/register.html")
    
def index(request):
    if request.user.is_authenticated:
        accounts = SocialMediaAccount.objects.filter(user=request.user)
        overview = {'Likes': 100, 'Account Views': 200}
        return render(request, 'Dashboard/index.html', {
            'accounts': accounts,
            'overview': overview
            })
    else:
        return render(request, 'Dashboard/login.html')


def connect_account(request):
    if request.method == 'POST':
        platform = request.POST['platform']
        username = request.POST['username']
        password = request.POST['password']  # Consider using OAuth instead of storing passwords

        # Check if the account already exists
        account = SocialMediaAccount.objects.filter(user=request.user, platform=platform).first()
        if account:
            # If the account exists, update the username and password
            account.username = username
            account.password = password
            account.save()
        else:
            # If the account does not exist, create a new one
            account = SocialMediaAccount(user=request.user, platform=platform, username=username, password=password)
            account.save()

        return HttpResponseRedirect(reverse('index'))
    else:
        # If the request is not a POST, redirect to the index page
        return HttpResponseRedirect(reverse('index'))
