from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.forms import inlineformset_factory
import random
from django.core.mail import send_mail
from app.forms import *
def home(request):
    return render(request,'index.html')
def signin(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username.title(),password=password)
        if user is not None:
            login(request,user)
            if username.title()=="Shiva":
                return redirect('admin')
            else:
                return redirect('home')
        else:
            messages.error(request,"Invalid login credentials")
    return render(request,'login.html')
def signup(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password1=request.POST['password1']
        if password!=password1 :
            messages.error(request,"Passwords not matches")
        elif User.objects.filter(username=username):
            messages.error(request,"Username already exists...!")
        elif User.objects.filter(email=email):
            messages.error(request,"Email already taken...!")
        elif len(password)<8:
            messages.error(request,"Password must be eight characters")
        else:
            User.objects.create_user(username=username.title(),email=email,password=password)
            user=authenticate(username=username.title(),password=password)
            # send_mail(
            #     'Signup message',
            #     f'Thank you {username} for Registering in Admission Management System ',
            #     'rsgmovie@gmail.com',
            #     [email],
            #     fail_silently=False
            # )
            if user is not None:
                login(request,user)
                return redirect('home')    
    return render(request,'signup.html')
no=0
email=''
def forgot(request):
    global email,no
    if request.method=='POST':
        email=request.POST['email']
        if User.objects.filter(email=email) and email!='':
            no=random.randint(19282,82727)
            send_mail(
                'Password Reset',
                f'Your verification code for password reset {no} \nDont share OTP with anyone',
                'rsgmovie@gmail.com',
                [email],
                fail_silently=False
            )
            return redirect('otp')
        else:   
            messages.error(request,'User does not exists')
            
    return render(request,"forgot.html")
ver=0
def otp(request):
    global no,email,ver
    if email=='' :
        return HttpResponse("<h1>You are not allowed</h1>")
    if request.method=='POST':
        otp=request.POST['otp']
        if otp==str(no):
            ver=1
            return redirect('reset')
        else:
            messages.error(request,'OTP is Incorrect')
    return render(request,'otp.html')
def reset(r):
    global email,no
    if email=='' or ver!=1:
        return HttpResponse("<h1>You are not allowed</h1>") 
    if r.method=='POST':
        password=r.POST['password']
        password1=r.POST['password1']
        if password!=password1:
            messages.error(r,"Passwords does not match")
        elif len(password)<8:
             messages.error(r,"Password must be 8 characters")
        else:
            user=User.objects.get(email=email)
            user.set_password(password)
            user.save()
            u=authenticate(username=user.username,password=password)
            if u is not None:
                login(r,u)
                return redirect('home')               
    return render(r,"reset.html")
def signout(request):
    logout(request)
    return redirect('home')
s=0
def student(request,id):
    form=Studentform()
    user=User.objects.get(id=id)
    global s
    if Students.objects.filter(username=user):
        s=Students.objects.get(username=user)
        form=Studentform(instance=s)
    if request.method=='POST':
        if request.POST['username'].title()!=str(user):
            messages.error(request,"Enter Correct username")
        elif Students.objects.filter(username=user):
            s=Students.objects.get(username=user)
            form=Studentform(request.POST,instance=s)
            if form.is_valid():
                form.save()
        else:
            form=Studentform(request.POST)
            if form.is_valid():
                form.save()
                
    return render(request,'student.html',{'form':form,'student':s})
def apply(request,id):
    form=inlineformset_factory(Students,Apply,fields=('branch','college'),can_delete=True,extra=3)
    s=Students.objects.get(id=id)
    app=s.apply_set.all()
    formset=form(queryset=Apply.objects.filter(student_id=id),instance=s)
    if request.method=="POST":
        formset=form(request.POST,instance=s)
        if formset.is_valid():
            formset.save()
            return redirect(f'/apply/{id}')
    return render(request,"apply.html",{'form':formset,'apply':app})

@user_passes_test(lambda u:u.is_superuser)
def admi(request):
    b=Institution.objects.all().count()
    a=Allotment.objects.all().count()
    c=Apply.objects.all().count()
    return render(request,"admin/home.html",{'all':a,'int':b,'pen':c})
@user_passes_test(lambda u:u.is_superuser)
def institutions(request):
    institution=0
    institutions=Institution.objects.order_by('code')
    if request.method=='POST':
        search=request.POST['search']
        if search!='' and Institution.objects.filter(code=search.upper()):
            institution=Institution.objects.get(code=search.upper())
    return render(request,'admin/institutions.html',{"institute":institutions,"i":institution})
@user_passes_test(lambda u:u.is_superuser)
def add(request):
    form=Instituteform()
    if request.method=='POST':
        form=Instituteform(request.POST)
        if Institution.objects.filter(code=request.POST['code'].upper()):
            messages.error(request,'Institute Already exists')
        else:
            if form.is_valid():
                form.save()
                return redirect('institutions')
    return render(request,'admin/add.html',{'form':form})
@user_passes_test(lambda u:u.is_superuser)
def delet(request,id):
    i=Institution.objects.get(id=id)
    i.delete()
    return redirect('institutions')
@user_passes_test(lambda u:u.is_superuser)
def edit(request,id):
    insti=Institution.objects.get(id=id)
    i=Instituteform(instance=insti)
    if request.method=='POST':
        i=Instituteform(request.POST,instance=insti)
        if i.is_valid():
            i.save()
            return redirect('institutions')

    return render(request,'admin/edit.html',{'form':i})
@user_passes_test(lambda u:u.is_superuser)
def select(request,id):
    s=Apply.objects.get(id=id)
    i=Institution.objects.get(code=s.college.code)
    if s.branch=='IT':
        i.it-=1
        i.save()
    if s.branch=='CSE':
        i.cse-=1
        i.save()
    if s.branch=='EEE':
        i.eee-=1
        i.save()
    if s.branch=='ECE':
        i.ece-=1
        i.save()
    if s.branch=='CIV':
        i.civ-=1
        i.save()
    if s.branch=='MEC':
        i.cs-=1
        i.save()
    user=User.objects.get(username=s.student.username)
    email=user.email
    send_mail(
                'Allotment Details',
                f'STUDENT DETAILS\n\nName:{s.student}\nHall Ticket:{s.student.hall_ticket}\nRank:{s.student.rank}\nCOLLEGE DETAILS\n\nCollege name:{s.college.name}\nCollege Code:{s.college.code}\nBranch:{s.branch}\nFee:{s.college.fee}',
                'rsgmovie@gmail.com',
                [email],
                fail_silently=False
            )
    m=Apply.objects.filter(student=s.student)
    Allotment(name=s.student,hall_ticket=s.student.hall_ticket,rank=s.student.rank,code=s.college.code,college=s.college.name,branch=s.branch,fee=s.college.fee).save()
    s.delete()
    m.delete()
    return redirect('approve')
@user_passes_test(lambda u:u.is_superuser)
def reject(request,id):
    s=Apply.objects.get(id=id)
    user=User.objects.get(username=s.student.username)
    send_mail(
                'Allotment Details',
                'You are not Allotted in any college',
                'rsgmovie@gmail.com',
                [user.email],
                fail_silently=False
            )
    m=Apply.objects.filter(student=s.student)
    s.delete()
    m.delete()
    return redirect('approve')
@user_passes_test(lambda u:u.is_superuser)
def approve(request):
    data=Apply.objects.order_by('student__rank')
    return render(request,"admin/approve.html",{'data':data})
@user_passes_test(lambda u:u.is_superuser)
def allotment(request):
    s=0
    student=Allotment.objects.order_by('rank')
    if request.method=='POST':
        search=request.POST['search']
        if  Allotment.objects.filter(hall_ticket=search.upper()):
            s=Allotment.objects.filter(hall_ticket=search.upper())
    return render(request,'admin/allotment.html',{'student':student,'s':s})
def allotments(request):
    s=0
    student=Allotment.objects.order_by('rank')
    if request.method=='POST':
        search=request.POST['search']
        if  Allotment.objects.filter(hall_ticket=search.upper()):
            s=Allotment.objects.filter(hall_ticket=search.upper())
    return render(request,'allotment.html',{'student':student,'s':s})
def institute(request):
    institution=0
    institutions=Institution.objects.order_by('code')
    if request.method=='POST':
        search=request.POST['search']
        if search!='' and Institution.objects.filter(code=search.upper()):
            institution=Institution.objects.get(code=search.upper())
    return render(request,'institute.html',{"institute":institutions,"i":institution})
def details(request,id):
    data=Institution.objects.get(id=id)
    return render(request,'details.html',{'i':data})
def profile(request):
    st=0
    s=User.objects.get(username=request.user)
    if Students.objects.filter(username=request.user):
        st=Students.objects.get(username=request.user)
    return render(request,"profile.html",{'user':s,'i':st})