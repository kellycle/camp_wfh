from django.shortcuts import render, redirect
from .models import User
import bcrypt
from django.contrib import messages

######################################################################################
#                                 Rendor HTML                                        *
######################################################################################

def index(request):
    return render(request, "home.html")

def success(request):
    if 'UserID' in request.session:
        context = {
            'thisUser': User.objects.get(id=request.session.get('UserID'))
        }
        return render(request, "success.html", context)
    
    return redirect ('/')

def create_account(request):
    if 'UserID' in request.session:
        context = {
            'thisUser': User.objects.get(id=request.session.get('UserID'))
        }
        return render(request, "success.html", context)
    else:
        return render (request, "create.html")

def login_page(request):
    if 'UserID' in request.session:
        return redirect('/success')
    else:
        return render (request, "login.html")  


######################################################################################
#                            Account Creation Methods                                *
######################################################################################

def add_user(request):
    # Code block for retrieving errors:
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect ('/')
    # Code block for checking passwords match:
    if request.POST['password'] == request.POST['confirm']:
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    else:
        return redirect ("/")
    # Code block for creating the new user:
    new_user = User.objects.create(
        fname = request.POST['fname'], 
        lname=request.POST['lname'], 
        email = request.POST['email'], 
        password = hashed_pw
    )
    # Code block for putting user in session and routing to user page:
    request.session['UserID'] = new_user.id

    return redirect('/dashboard')


def login(request):
    #Code block for retrieving errors 
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect ('/')
    #Code block for checking user session and if passwords match, redirecting dashboard
    existingUser = User.objects.filter(email = request.POST['email']).first()
    if existingUser is not None:
        if bcrypt.checkpw(request.POST['password'].encode(), existingUser.password.encode()):
            request.session['UserID'] = existingUser.id
            return redirect('/success')
        else:
            print('password does not match')
    else:
        print('user does not exist')
    return redirect('/did not log in')


def log_out(request):
    request.session.clear()
    return redirect('/')

######################################################################################
#                                    Action Methods                                  *
######################################################################################