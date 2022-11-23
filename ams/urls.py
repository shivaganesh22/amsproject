"""ams URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('accounts/login/',signin,name='signin'),
    path('signup/',signup,name='signup'),
    path('forgotpassword/',forgot,name='forgot'),
    path('reset/',reset,name='reset'),
    path('reset/otp',otp,name='otp'),
    path('logout/',signout,name='signout'),
    path('student/<int:id>',student,name='student'),
    path('apply/<int:id>/',apply,name='apply/'),
    path('a/',admi,name='admin'),
    path('a/edit/<int:id>',edit,name='edit'),
    path('a/delete/<int:id>',delet),
    path('a/select/<int:id>',select),
    path('a/reject/<int:id>',reject),
    path('a/add',add,name='add'),
    path('a/institutions',institutions,name='institutions'),
    path('a/approve',approve,name='approve'),
    path('a/allotments/',allotment,name='allotment'),
    path('allotments/',allotments,name='allotment'),
    path('institutions',institute,name='institute'),
    path('view/<int:id>',details,name='details'),
    path('profile/',profile,name='profile'),
]
