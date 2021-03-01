from django.urls import path     
from . import views


######################################################################################
#                                Rendor Routes                                       *
######################################################################################

urlpatterns = [
    path('', views.index),
    path('dashboard', views.success),
    path('create_account', views.create_account),
    path('success', views.success),
    path('loginpage', views.login_page),

######################################################################################
#                                 Action Routes                                      *
######################################################################################

    path('adduser', views.add_user),
    path('login', views.login), 	  
    path('logout', views.log_out), 
]