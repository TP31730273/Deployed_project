from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from .models import *
from random import randint

default_data = {
    'form_membership': ['login', 'register', 'reset_pass'],

}

# serialize function 

def seri(model_object):
    d={}
    for k,v in model_object.__dict__.items():
        if k.startswith('_') or k.endswith('_'):
            continue
        d.setdefault(k,v)
    return d

def login(request):
    if 'email' in request.session:
        return redirect(profile)
    
    default_data['current_page'] = 'login'
    return render(request, 'todoapp/login.html', default_data)


def index(request):
    return redirect(login)


def register(request):
    default_data['current_page'] = 'register'
    return render(request, 'todoapp/register.html', default_data)


def reset_pass(request):
    default_data['current_page'] = 'reset_pass'
    return render(request, 'todoapp/recovery-password.html', default_data)

# profile data
def profile_data(request):
    master= Master.objects.get(Email=request.session['email'])
    profile=Profile.objects.get(Master= master)
    
    load_connection(request)    
    default_data['profile_data']=seri(profile)
    default_data['gender_choice']=[{'short_val': i, 'text' : j} for i,j in choice_gender]

def profile(request):
    profile_data(request)
    default_data['current_page'] = 'profile'
    return render(request, 'todoapp/profile.html', default_data)
# update profile data 

def profile_update(request):
    master= Master.objects.get(Email=request.session['email'])
    profil=Profile.objects.get(Master= master)
    profil.FullName=request.POST['fname']
    profil.Mobile=request.POST['phone']
    profil.Gender=request.POST['gender']
    x=request.POST['dob']
    
    # j=x.split('/')
    # t=str(j[2])+'-'+str(j[0])+'-'+str(j[1])
    
    # profil.Birthdate=x
    profil.City=request.POST['city']
    profil.State=request.POST['state']
    profil.Country=request.POST['country']
    profil.Address=request.POST['address']
    profil.save()

    profile_data(request)
    default_data['t']=x
    return JsonResponse(default_data)

# change password
def change_password(request):
    master= Master.objects.get(Email=request.session['email'])
    old_pwd=request.POST['old_password']    
    new_pwd=request.POST['new_password']    
    if master.Password == old_pwd:
        master.Password = new_pwd
        master.save()
        print("password change successfully ")
        return redirect(profile)
    else:
        msg="password incorrect please enter again"
        print(msg)
        del request.session['email']
        return redirect(login)


# register data

# create reference id

def reg_data(request):
    master = Master.objects.create(Email=request.POST['email'],Password=request.POST['password'])

    ref_id=f"{request.POST['email'].split('@')[0]}{randint(1000,9999)}"
    print("reference id: ",ref_id)
    Profile.objects.create(Master=master,RefID=ref_id)
    print("user registrated sussessfully")
    return redirect(register)
    
    

# login functionality

def login_data(request):
    eml=request.POST['email']
    password=request.POST['password']
    
    try:
        master= Master.objects.get(Email=eml)
        if master.Password == password:
            request.session['email']=eml
            print("login sucess",master)
            return redirect(profile)
        else:
            msg="Username of password incorrect please enter again"
            print(msg)
           
    except Master.DoesNotExist:
        print(f"{eml} does not exist please register it.")
    return redirect(login)




# search reference
def search_ref(request):
    profile= Profile.objects.get(RefID=request.POST['refid'])
    default_data['ref_data']= seri(profile)
    default_data['msg']='reference succcessfully found'
    return JsonResponse(default_data)
    
 
# request new connection

def request_connection(request):
    master= Master.objects.get(Email=request.session['email'])
    profile= Profile.objects.get(RefID=request.POST['refid'])
    
    connection.objects.create(Master=master, Profile=profile)

# create todo
def create_todo(request):
    master= Master.objects.get(Email=request.session['email'])
    profile= Profile.objects.get(RefID=request.POST['refid'])
    

# load connection

def load_connection(request):
    master= Master.objects.get(Email=request.session['email'])
    Connections=connection.objects.filter(Master=master)
    default_data['myconnections']=Connections

    pass
# add new connection
def add_connection(request):
    master= Master.objects.get(Email=request.session['email'])
    profile= Profile.objects.get(Master=master)

    Connection=connection.objects.get(Profile=profile)
    Connection.status = 'active'

# sign-out
def sign_out(request):
    if 'email' in request.session:
        del request.session['email']
    
    return redirect(login)
    