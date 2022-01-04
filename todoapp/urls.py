from django.urls import path
from .views import *

urlpatterns = [
    
    path('',login,name="login"),
    path('index/',index,name="index"),
    path('register/',register,name="register"),
    path('reset_pass/',reset_pass,name="reset_pass"),
    path('profile/',profile,name="profile"),
    path('reg_data/',reg_data,name="reg_data"),
    path('login_data/',login_data,name="login_data"),
    path('sign_out/',sign_out,name="sign_out"),
    path('profile_update/',profile_update,name="profile_update"),
    path('change_password/',change_password,name="change_password"),
    path('search_ref/',search_ref,name="search_ref"),


    # path('form_data/',form_data,name="form_data"),

]
