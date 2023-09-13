from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from datetime import date
# Create your views here.

def Home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    error = ""
    if request.method == 'POST':
        n = request.POST['name']
        e = request.POST['email']
        mn = request.POST['mobnum']
        msg = request.POST['message']
        try:
            Contact.objects.create(name=n, contact=mn, emailid=e,message=msg,mdate=date.today(),isread="no")
            error = "no"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'contact.html',d)

def adminlogin(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['password']
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request, user)
                error="no"
            else:
                error = "yes"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'login.html',d)

def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    donor = Donor.objects.all()
    td =0


    for i in donor:
        td+=1


    contact = Contact.objects.all()
    tuq = 0
    trq = 0

    for i in contact:
        if i.isread == "yes":
            trq += 1
        elif i.isread == "no":
            tuq += 1

    d = {'td':td,'tuq':tuq,'trq':trq}
    return render(request,'admin_home.html',d)


def Logout(request):
    logout(request)
    return redirect('home')


def changepassword(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error = ""
    if request.method=="POST":
        o = request.POST['currentpassword']
        n = request.POST['newpassword']
        c = request.POST['confirmpassword']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            error = "yes"
        else:
            error = "not"
    d = {'error':error}
    return render(request,'changepassword.html',d)


def unread_queries(request):
    if not request.user.is_authenticated:
        return redirect('login')
    contact = Contact.objects.all()
    d = {'contact': contact}
    return render(request, 'unread_queries.html', d)

def read_queries(request):
    if not request.user.is_authenticated:
        return redirect('login')
    contact = Contact.objects.all()
    d = {'contact': contact}
    return render(request, 'read_queries.html', d)


def view_queries(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    contact = Contact.objects.get(id=pid)
    contact.isread = "yes"
    contact.save()
    d = {'contact':contact}
    return render(request, 'view_queries.html', d)


def add_bloodgroup(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error = ""
    if request.method=="POST":
        bg = request.POST['bloodgroup']

        try:
            Group.objects.create(bloodgroup=bg)
            error = "no"
        except:
            error = "yes"
    d = {'error':error}
    return render(request, 'add_bloodgroup.html', d)


def view_bloodgroup(request):
    if not request.user.is_authenticated:
        return redirect('login')
    group = Group.objects.all()
    d = {'group': group}
    return render(request, 'view_bloodgroup.html', d)

def delete_bloodgroup(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    group = Group.objects.get(id=pid)
    group.delete()
    return redirect('view_bloodgroup')


def add_donor(request):
    if not request.user.is_authenticated:
        return redirect('login')
    group = Group.objects.all()
    error = ""
    if request.method=="POST":
        fn = request.POST['fullname']
        con = request.POST['contact']
        eid = request.POST['emailid']
        a = request.POST['age']
        g = request.POST['gender']
        bg = request.POST['bloodgroup']
        addr = request.POST['address']
        msg = request.POST['message']
        group1 = Group.objects.get(bloodgroup=bg)
        bdate = date.today()
        try:
            Donor.objects.create(fullname=fn,mobileno=con,emailid=eid,
                                 gender=g,age=a,group=group1,
                                 address=addr,message=msg,postingdate=bdate)
            error = "no"
        except:
            error = "yes"
    d = {'error':error,'group':group}
    return render(request, 'add_donor.html', d)


def donorlist(request):
    if not request.user.is_authenticated:
        return redirect('login')
    donor = Donor.objects.all()
    d = {'donor': donor}
    return render(request, 'donorlist.html', d)

def delete_donor(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    donor = Donor.objects.get(id=pid)
    donor.delete()
    return redirect('donorlist')


def view_donordetail(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    donor = Donor.objects.filter(id=pid)
    d = {'donor':donor}
    return render(request, 'view_donordetail.html', d)

def user_search(request):
    if not request.user.is_authenticated:
        return redirect('login')
    terror = ""
    contact=""
    sd=""
    if request.method == "POST":
        sd = request.POST['searchdata']
        try:
            contact = Contact.objects.filter(Q(name=sd)|Q(contact=sd))
            terror = "found"
        except:
            terror="notfound"
    d = {'contact':contact,'terror':terror,'sd':sd}
    return render(request,'user_search.html',d)


def blood_search(request):
    terror = ""
    donor=""
    sd=""
    if request.method == "POST":
        sd = request.POST['searchblood']
        try:
            group = Group.objects.get(bloodgroup=sd)
            donor = Donor.objects.filter(Q(group=group)|Q(address=sd))
            terror = "found"
        except:
            terror="notfound"
    d = {'donor':donor,'terror':terror,'sd':sd}
    return render(request,'blood_search.html',d)


def booking_search(request):
    if not request.user.is_authenticated:
        return redirect('login')
    terror = ""
    donor=""
    sd=""
    if request.method == "POST":
        sd = request.POST['searchdonor']
        try:
            donor = Donor.objects.filter(Q(fullname=sd)|Q(mobileno=sd)|Q(id=sd))
            terror = "found"
        except:
            terror="notfound"
    d = {'donor':donor,'terror':terror,'sd':sd}
    return render(request,'booking_search.html',d)

def bookingbtwdates(request):
    if not request.user.is_authenticated:
        return redirect('login')
    """booking=""
    if request.method=="POST":
        fd = request.POST['fromdate']
        td = request.POST['todate']
        booking = Booking.objects.filter(Q(bookingdate__gte=fd) & Q(bookingdate__lte=td))
    d = {'booking':booking}"""
    return render(request, 'bookingbtwdates.html')




def betweendate_report(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == "POST":
        fd = request.POST['fromdate']
        td = request.POST['todate']
        donor = Donor.objects.filter(Q(postingdate__gte=fd) & Q(postingdate__lte=td))
        d = {'donor':donor,'fd':fd,'td':td}
        return render(request, 'bookingbtwdates.html', d)
    return render(request, 'betweendate_report.html')


def becomedonor(request):
    group = Group.objects.all()
    error = ""
    if request.method=="POST":
        fn = request.POST['fullname']
        con = request.POST['contact']
        eid = request.POST['emailid']
        a = request.POST['age']
        g = request.POST['gender']
        bg = request.POST['bloodgroup']
        addr = request.POST['address']
        msg = request.POST['message']
        group1 = Group.objects.get(bloodgroup=bg)
        bdate = date.today()
        try:
            Donor.objects.create(fullname=fn,mobileno=con,emailid=eid,
                                 gender=g,age=a,group=group1,
                                 address=addr,message=msg,postingdate=bdate)
            error = "no"
        except:
            error = "yes"
    d = {'error':error,'group':group}
    return render(request, 'becomedonor.html', d)


