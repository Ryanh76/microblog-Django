#views.py
from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from models import posts
from mongoengine.django.auth import User

# Create your views here.

def IndexView(request):
    all_post = posts.objects.order_by('-time')
    if request.method == 'GET':
        return render(request, 'index.html',{'all_post': all_post})

    if request.method == 'POST':
        try:
            new_post = posts(user = str(request.user),
                             post = str(request.POST['post']),
                             time = datetime.now()
                            )
            new_post.save()
            messages.success(request, "new post added")
            return redirect('/microblog')
        except:
            messages.error(request, "create post error")
            return redirect('/microblog')

def RegView(request):
    if request.method == 'GET':
        return render(request, 'reg.html')

    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            passwordrepeat = request.POST['password-repeat']

            if User.objects(username=username).first():
                messages.error(request, "user exists")
                return redirect("reg.html")
            elif password != passwordrepeat:
                messages.error(request, "please enter same password")
                return redirect("reg.html")
            else:
                user = User.create_user(username = username, password = password)
                messages.success(request, "user register successfully")
                return render(reqeuest, 'user.html')
        except:
            messages.error(request, "Error, please try again")
            return redirect("reg.html")

@login_required()
def UserView(request, user):
    all_post = posts.objects(user= str(request.user)).order_by('-time')
    if request.method == 'GET':
        return render(request, 'user.html',{'all_post': all_post})

    if request.method == 'POST':
        try:
            new_post = posts(user = str(request.user),
                             post = str(request.POST['post']),
                             time = datetime.now()
                            )
            new_post.save()
            messages.success(request, "new post added")
            return redirect('/microblog/u/%s' % (user) )
        except:
            messages.error(request, "create post error")
            return redirect('/microblog/u/%s' % (user) )

def LoginView(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            user = User.objects.get(username=username)
            if user.check_password(password):
                user.backend = 'mongoengine.django.auth.MongoEngineBackend'
                user = authenticate(username=username, password=password)
                login(request, user)
                request.session.set_expiry(360000)
                messages.success(request, 'Welcome to microblog')
                return redirect('/microblog/u/%s' % (username) )
            else:
                 messages.error(request, 'Please check your password')
                 return redirect('login.html')
        except User.DoesNotExist:
            messages.error(request, 'User doesn\'t exist')
            return redirect('login.html')

        #except:
        #    messages.error(request, 'Login failure')
        #    return render(request, 'index.html')

@login_required()
def LogoutView(request):
    logout(request)
    messages.success(request, 'Logout successfully.')
    #return render(request, 'index.html')
    return redirect('/microblog/')

