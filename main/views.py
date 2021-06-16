from django.shortcuts import render, get_object_or_404, redirect
from .models import Main
from news.models import News
from cat.models import Cat  # for showing categories in footer
from subcat.models import SubCat  ## for SubMenu in the menu bar
from django.contrib.auth import authenticate, login, logout  # for authentication
from django.core.files.storage import FileSystemStorage  # for upload image
from trending.models import Trending  ### Trending app's model
import random                   ## Random Object (For Trending now)
from random import randint      ## Random Object (For Trending now)
from django.contrib.auth.models import User, Group, Permission
from manager.models import Manager
import string
import ipaddress


# Create your views here.


##--#--## Home Page(home) Function For Front (User Interface - Frontend) Start ##--#--##
def home(request):
    # sitename = "MySite | Home"     
    # return render(request, 'front/home.html', {'sitename':sitename})
    
    site = Main.objects.get(pk=2)
    news = News.objects.filter(act=1).order_by('-pk')  ## for reverse(ordering) need to filter by pk with (-) to get the latest submission first.

    cat = Cat.objects.all()  ## Show categories in footer
    subcat = SubCat.objects.all()  ## for SubMenu in the menu bar
    
    lastnews = News.objects.filter(act=1).order_by('-pk')[:3]   ### This query for last three post

    popnews = News.objects.filter(act=1).order_by('-show')    ### Populer News will be Shown according to view(show)

    popnews2 = News.objects.filter(act=1).order_by('-show')[:3]    ### 3 Populer News will be Shown according to view(show) in footer section

    trending = Trending.objects.all().order_by('-pk')[:3] ### Trending now will show on top bar(send query from here to naster.html in front)

    lastnews2 = News.objects.filter(act=1).order_by('-pk')[:4] # Last Four News in Three Different Frames

    random_object = Trending.objects.all()[randint(0, len(trending) -1)] ## Random Object (For Trending now). I just used it for home page. To show the trending randomly
    # print(random_object)
    return render(request, 'front/home.html', {'site':site, 'news':news, 'cat':cat, 'subcat':subcat, 'lastnews':lastnews, 'popnews':popnews, 'popnews2':popnews2, 'trending':trending, 'lastnews2':lastnews2})
##--#--## Home Page(home) Function For Front (User Interface - Frontend) End ##--#--##


##--#--## About Page(about) Function For Front (User Interface - Frontend) Start ##--#--##
def about(request):

    site = Main.objects.get(pk=2)

    news = News.objects.all().order_by('-pk')  ## for reverse(ordering) need to filter by pk with (-) to get the latest submission first.

    cat = Cat.objects.all()  ## Show categories in footer
    subcat = SubCat.objects.all()  ## for SubMenu in the menu bar
    
    lastnews = News.objects.all().order_by('-pk')[:3]   ### This query for last three post

    popnews2 = News.objects.all().order_by('-show')[:3]    ### 3 Populer News will be Shown according to view(show) in the footer section and sidebar on the right.

    trending = Trending.objects.all().order_by('-pk')[:3] ### Trending now will show on top bar(send query from here to naster.html in front)

    return render(request, 'front/about.html', {'site':site, 'news':news, 'cat':cat, 'subcat':subcat, 'lastnews':lastnews, 'popnews2':popnews2, 'trending':trending})
##--#--## About Page(about) Function For Front (User Interface - Frontend) End ##--#--##


##--#--## Panel (Admin Panel) Function For Back (Admin Panel - Backend) Start ##--#--##
def panel(request):

    # Login check Start
    if not request.user.is_authenticated:
        return redirect('mylogin')   # when user is not logged in, it will take you the login page(mylogin)
    # Login check End

# Permission Check(logged in user can access or not) Start
    perm = 0
    perms = Permission.objects.filter(user=request.user) ## Current user, that is logged in now
    for i in perms :
        if i.codename == "master_user" : perm = 1

    '''
    # random string algo Start
    test = ['!', '@', '#', '$', '%']
    rand = ""
    for i in range(4): # 4*3 = total 12. 3 means letter,number,special
        rand = rand + random.choice(string.ascii_letters)
        rand += random.choice(test)
        rand += str(random.randint(0, 9))
    # random string algo End
    '''

    #-# Random Name Of The News (string for dashboard) Start
    count = News.objects.count()
    rand = News.objects.all()[random.randint(0, count-1)]
    #-# Random Name Of The News (string for dashboard) End

    # if perm == 0 :
    #     error = "Access Denied"
    #     return render(request, 'back/error.html', {'error':error})

# Permission Check(logged in user can access or not) End

    return render(request, 'back/home.html', {'rand':rand})
##--#--## Panel (Admin Panel) Function For Back (Admin Panel - Backend) End ##--#--##


##--#--## LogIn (mylogin) Function For Front (User Interface - Frontend) Start ##--#--##
def mylogin(request):

    if request.method == 'POST':

        utxt = request.POST.get('username')   # utxt to get/receive the username
        ptxt = request.POST.get('password')   # ptxt to get/receive the password   

        if utxt != "" and ptxt != "":

            user = authenticate(username=utxt, password=ptxt) 

            if user != None:

                login(request, user)
                return redirect('panel')

    return render(request, 'front/login.html')
##--#--## LogIn (mylogin) Function For Front (User Interface - Frontend) End ##--#--##


##--#--## Registration (myregister) Function For Front (User Interface - Frontend) Start ##--#--##
def myregister(request):

    if request.method == 'POST':
        
        name = request.POST.get('name')
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if name == "" :
            msg = "Input Your Name"
            return render(request, 'front/msgbox.html', {'msg':msg})

        if password1 != password2 :
            msg = "Your Password Didn't Match"
            return render(request, 'front/msgbox.html', {'msg':msg})

    #-# Check Password is Weak or Strong (by using count) Start #-#
        count1 = 0
        count2 = 0
        count3 = 0
        count4 = 0
        for i in password1 :
            ## I defined here 4 counts
            ## if any user enter 10 char, count will change from 1 to 1 and it won't increase
            ## If my count 1 2 3 and 4 were all 1 then my password is a strong password
            if i > "0" and i < "9" :
                count1 = 1              ## one number, count will change from 0 to 1
            if i > "A" and i < "Z" :
                count2 = 1              ## one cap letter, count will change from 0 to 1
            if i > "a" and i < "z" :
                count3 = 1              ## one small letter, count will change from 0 to 1
            if i > "!" and i < "(" :
                count4 = 1              ## one sign, count will change from 0 to 1
            ## if enter number,cap,small,sign(count 1 1 1 1). if enter number,small(count 1 0 1 0) ## 
        if count1 == 0 or count2 == 0 or count3 == 0 and count4 == 0 :
            msg = "Your Password Is Not Strong Enough"
            return render(request, 'front/msgbox.html', {'msg':msg})
    #-# Check Password is Weak or Strong (by using count) End #-#
        if len(password1) < 8 :
            msg = "Your Password Must Be At Least 8 Characters"
            return render(request, 'front/msgbox.html', {'msg':msg})

        if len(User.objects.filter(username=uname)) == 0 and len(User.objects.filter(email=email)) == 0 :

            # Get User IP Start
            ip, is_routable = get_client_ip(request)

            if ip is None:
                ip = "0.0.0.0"
            # Get User IP End
            # Get User Location Start
            try:
                response = DbIpCity.get(ip, api_key='free')
                country = response.country + " | " + response.city

            except:
                country = "Unknown"
            # Get User Location End
            
            user = User.objects.create_user(username=uname, email=email, password=password1)
            b = Manager(name=name, utxt=uname, email=email, ip=ip, country=country)
            b.save()

    return render(request, 'front/login.html')
##--#--## Registration (myregister) Function For Front (User Interface - Frontend) End ##--#--##


##--#--## Log Out Start ##--#--##
def mylogout(request):

    logout(request)

    return redirect('mylogin')
##--#--## Log Out End ##--#--##



##--#--## Site Settings (Topbar, fb/yt/tw link, logo etc) Function For Back (Admin Panel - Backend) Start ##--#--##
def site_setting(request):

    # Login check Start
    if not request.user.is_authenticated:
        return redirect('mylogin')   # when user is not logged in, it will take you the login page(mylogin)
    # Login check End

    #-# Masteruser Access Start #-#
    perm = 0
    for i in request.user.groups.all() :
        if i.name == "masteruser" : perm = 1

    if perm == 0 :
        error = "Access Denied"
        return render(request, 'back/error.html', {'error':error})
    #-# Masteruser Access End #-#

    if request.method == 'POST':
        ## Values saved start
        name = request.POST.get('name')
        tell = request.POST.get('tell')
        fb = request.POST.get('fb')
        tw = request.POST.get('tw')
        yt = request.POST.get('yt')
        link = request.POST.get('link')
        txt = request.POST.get('txt')
        ## Values saved end

        ## To control social media Start
        if fb == "" : fb = "#"  # hashtag would be automatically set inside it
        if tw == "" : tw = "#"
        if yt == "" : yt = "#"
        if link == "" : link = "#"
        ## To control social media End

        if name == "" or tell == "" or txt == "":
            error = "All Fields Required"
            return render(request, 'back/error.html', {'error':error})

        ## First logo ##
        try:
            #-#-# Upload File Start #-#-#
            myfile = request.FILES['myfile']  # upload file
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)  # it will change the file name if already exist
            url = fs.url(filename)
            #-#-# Upload File End #-#-#

            picurl = url
            picname = filename


        except:

            picurl = "-"
            picname = "-"

        ## Second Logo ##
        try:
            #-#-# Upload File Start #-#-#
            myfile2 = request.FILES['myfile2']  # upload file
            fs2 = FileSystemStorage()
            filename2 = fs2.save(myfile2.name, myfile2)  # it will change the file name if already exist
            url2 = fs2.url(filename2)
            #-#-# Upload File End #-#-#

            picurl2 = url2
            picname2 = filename2


        except:

            picurl2 = "-"
            picname2 = "-"

            
        b = Main.objects.get(pk=2)
        b.name = name
        b.tell = tell
        b.fb = fb
        b.tw = tw
        b.yt = yt
        b.link = link
        b.about = txt   # about is the field name

        if picurl != "-" : b.picurl = picurl        
        if picname != "-" : b.picname = picname
        if picurl2 != "-" : b.picurl2 = picurl2      
        if picname2 != "-" : b.picname2 = picname2       
        
        b.save()

    site = Main.objects.get(pk=2)

    return render(request, 'back/setting.html', {'site':site})
##--#--## Site Settings (Topbar, fb/yt/tw link, logo etc) Function For Back (Admin Panel - Backend) End ##--#--##


##--#--## Text Change in About Page(Change from admin panel) Start ##--#--##
def about_setting(request):

    # Login check Start
    if not request.user.is_authenticated:
        return redirect('mylogin')   # when user is not logged in, it will take you the login page(mylogin)
    # Login check End

    #-# Masteruser Access Start #-#
    perm = 0
    for i in request.user.groups.all() :
        if i.name == "masteruser" : perm = 1

    if perm == 0 :
        error = "Access Denied"
        return render(request, 'back/error.html', {'error':error})
    #-# Masteruser Access End #-#

    if request.method == 'POST':
        txt = request.POST.get('txt')

        if txt == "":   ## when text is empty, it will show the error page
            error = "All Fields Required"
            return render(request, 'back/error.html', {'error':error})

        b = Main.objects.get(pk=2)
        b.abouttxt = txt
        b.save()

    about = Main.objects.get(pk=2).abouttxt  ## abouttxt is model field name

    return render(request, 'back/about_setting.html', {'about': about})
##--#--## Text Change in About Page(change from admin panel) End ##--#--##


##--#--## Contact Page (contact) Function For Front (User Interface - Frontend) Start ##--#--##
def contact(request):
    ##--## For Logo, Categories, Sub-Categories, Footer etc Start ##--##
    site = Main.objects.get(pk=2)
    news = News.objects.all().order_by('-pk')  ## for reverse(ordering) need to filter by pk with (-) to get the latest submission first.
    cat = Cat.objects.all()  ## Show categories in footer
    subcat = SubCat.objects.all()  ## for SubMenu in the menu bar    
    lastnews = News.objects.all().order_by('-pk')[:3]   ### This query for last three post
    popnews2 = News.objects.all().order_by('-show')[:3]    ### 3 Populer News will be Shown according to view(show) in the footer section and sidebar on the right.
    ##--## For Logo, Categories, Sub-Categories, Footer etc End ##--##
    trending = Trending.objects.all().order_by('-pk')[:3] ### Trending now will show on top bar(send query from here to naster.html in front)

    return render(request, 'front/contact.html', {'site':site, 'news':news, 'cat':cat, 'subcat':subcat, 'lastnews':lastnews, 'popnews2':popnews2, 'trending':trending})
##--#--## Contact Page (contact) Function For Front (User Interface - Frontend) End ##--#--##    


##--#--## Password Change (change from admin panel) Start ##--#--##
def change_pass(request):

    # Login check Start
    if not request.user.is_authenticated:
        return redirect('mylogin')   # when user is not logged in, it will take you the login page(mylogin)
    # Login check End

    if request.method == 'POST' :
              
        oldpass = request.POST.get('oldpass')
        newpass = request.POST.get('newpass')

        if oldpass == "" or newpass == "" :
            error = "All Fields Required"
            return render(request, 'back/error.html', {'error':error})

        user = authenticate(username=request.user, password=oldpass)
        if user != None:

            if len(newpass) < 8 :
                error = "Your Password Must Be At Least 8 Characters"
                return render(request, 'back/error.html', {'error':error})

        #-# Check Password is Weak or Strong (by using count) #-#
            count1 = 0
            count2 = 0
            count3 = 0
            count4 = 0
            for i in newpass :
                ## I defined here 4 counts
                ## if any user enter 10 char, count will change from 1 to 1 and it won't increase
                ## If my count 1 2 3 and 4 were all 1 then my password is a strong password
                if i > "0" and i < "9" :
                    count1 = 1              ## one number, count will change from 0 to 1
                if i > "A" and i < "Z" :
                    count2 = 1              ## one cap letter, count will change from 0 to 1
                if i > "a" and i < "z" :
                    count3 = 1              ## one small letter, count will change from 0 to 1
                if i > "!" and i < "(" :
                    count4 = 1              ## one sign, count will change from 0 to 1
                ## if enter number,cap,small,sign(count 1 1 1 1). if enter number,small(count 1 0 1 0) ## 
            
            if count1 == 1 and count2 == 1 and count3 == 1 and count4 == 1 : # That means password is strong 
                
                user = User.objects.get(username=request.user)
                user.set_password(newpass)
                user.save()
                return redirect('mylogout')
        
        else:
            error = "Your Password Is Not Correct"
            return render(request, 'back/error.html', {'error':error})

    return render(request, 'back/change_pass.html')
##--#--## Password Change (change from admin panel) End ##--#--##