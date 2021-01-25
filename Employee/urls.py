from django.urls import path,include
from .views import *


urlpatterns = [
    
    # path('',home,name='home' ),
    # # path('register/',register,name='register'),
    # path('register/',employee_add,name='register'),
    # path('user_login/',user_login,name='user_login'),
    # path('user_logout/',user_logout,name='user_logout'),

    path('',EmployeeCRUDSingleEndpoint.as_view()),
    path('auth/',LoginLogoutApi.as_view()),
]
