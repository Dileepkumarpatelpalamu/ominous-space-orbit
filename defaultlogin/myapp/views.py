from __future__ import unicode_literals
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from myapp.models import *
from .forms import *
from django.contrib.auth.hashers import make_password,check_password
from datetime import date
from django.contrib import messages
from django.core.mail import send_mail

# Create your views here.

def homepage(request):
    if request.session.get('email'):
        email= request.session.get('email')
        context={'profiles':Profile.get_profiles(email)}
        id = context['profiles'].id
        context['qualifications'] = Qualification.get_qualification(id)
        context['personaldata'] = PersonalDetail.get_data(id)
        context['techskills'] = TechnicalSkill.techskill(id)
        context['links'] = PasswordData.get_link(id)
    else:
        context={'profiles':Profile.get_profiles()}
        id = context['profiles'].id
        context['qualifications'] = Qualification.get_qualification(id)
        context['personaldata'] = PersonalDetail.get_data(id)
        context['techskills'] = TechnicalSkill.techskill(id)
        context['links'] = PasswordData.get_link(id)
    return render(request,'homepage.html',context)
def userlogin(request):
    context ={'forms':LoginForm(request.GET)}
    return render(request,'login.html',context)
def userloginpost(request):
    if request.method == 'POST':
        fmdata = LoginForm(request.POST)
        if fmdata.is_valid():
            email = fmdata.cleaned_data.get('email')
            user = Profile.get_login(email)
            if not user:
                messages.error(request,'User authentication fails..!')
                return redirect('/login/')
            userpass = PasswordData.get_password(user.id)
            if not userpass:
                messages.error(request,'User authentication fails..!')
                return redirect('/login/')
            password = fmdata.cleaned_data.get('password')
            if check_password(password,userpass.password):
                messages.success(request,"Your logged in successfully")
                request.session['name']= user.name
                request.session['email'] = user.email
                request.session['phone'] = user.phone
                return redirect('homepage')
            else:
                messages.error(request,'User authentication fail due wrong password')
                return redirect('/login/')
        else:
            context={'forms':fmdata}
            return render(request,'login.html',context)
    else:
        return redirect('/login/')
def usersignup(request):
    context={'forms':SignupForm(request.GET)}
    return render(request,'signin.html',context)
def usersignuppost(request):
    if request.method == 'POST':
        fmdata = SignupForm(request.POST)
        if fmdata.is_valid():
            name = fmdata.cleaned_data.get('name')
            email =fmdata.cleaned_data.get('email')
            phone =fmdata.cleaned_data.get('phone')
            password =fmdata.cleaned_data.get('password')
            dt = date.today()
            reg = Profile.objects.create(name=name,email=email,phone=phone,date=dt)
            passid = PasswordData(profile_id=reg.id,password=password)
            passid.password = make_password(passid.password)
            passid.save()
            reg.save()
            messages.success(request,'You are registered successfully..!')
            return redirect('/login/')
        else:
            context={'forms':fmdata}
            return render(request,'signin.html',context)
    else:
        return redirect('/signup/')
def userlogout(request):
    if request.session.get('email'):
        del request.session['email']
        del request.session['name']
        del request.session['phone']
        messages.success(request,'Your are logged out successfully ..!')
    return redirect('login')
def getprofileupdate(request):
    email = request.session.get('email')
    profiles = Profile.objects.filter(email=email).values('name','title','phone','career')
    context={'forms':ProfileUpdateForm(initial=profiles[0])}
    return render(request,'profileupdate.html',context)
def postprofileupdate(request):
    if request.method=="POST":
        fmdata = ProfileUpdateForm(request.POST,request.FILES)
        if fmdata.is_valid():
            name = fmdata.cleaned_data.get('name')
            title = fmdata.cleaned_data.get('title')
            phone = fmdata.cleaned_data.get('phone')
            career = fmdata.cleaned_data.get('career')
            photo = request.FILES['photo']
            profile = Profile.get_profiles(request.session.get('email'))
            print(profile.id)
            updateprofile = Profile.objects.filter(id=profile.id)
            data = updateprofile.update(name=name,title=title,phone=phone,career=career,photo=photo)
            messages.success(request,'Your profiles updated successfully..!')
            return redirect('homepage')
        else:
            messages.error(request,'Profiles updating fail...!')
            context ={'forms':fmdata}
            return render(request,'profileupdate.html',context)
    else:
        return redirect('getprofileupdate')
def getsocialupdate(request):
    email = request.session.get('email')
    if email:
        proid = Profile.get_profiles(email)
        social_links = PasswordData.objects.filter(profile_id=proid.id).values('linkin','git_link','wb_link')
        context ={'forms':SocialUpdateForm(initial=social_links[0])}
        return render(request,'socialupdate.html',context)
    return redirect('homepage')
def postsocialupdate(request):
    if request.method=="POST" and request.session.get('email'):
        email = request.session.get('email')
        fmdata = SocialUpdateForm(request.POST)
        if fmdata.is_valid():
            linkin = fmdata.cleaned_data.get('linkin')
            git_link = fmdata.cleaned_data.get('git_link')
            wb_link = fmdata.cleaned_data.get('wb_link')
            proid = Profile.get_profiles(email)
            socialupdate = PasswordData.objects.filter(profile_id=proid.id)
            socialupdate.update(linkin=linkin,git_link=git_link,wb_link=wb_link)
            messages.success(request,'Social link updated successfullt..!')
            return redirect('homepage')
        else:
            context={'forms':fmdata}
            messages.error(request,'Please enter valid url or links')
            return render(request,'socialupdate.html',context)

    else:
        return redirect('homepage')
def getqulificationupdate(request):
    if request.session.get('email'):
        context={'forms':QulificationForm()}
        return render(request,'qulificationadd.html',context)
    else:
        return redirect('homepage')
def postqulificationupdate(request):
    email = request.session.get('email')
    if request.method == 'POST' and email:
        proid = Profile.get_profiles(email)
        fmdata = QulificationForm(request.POST)
        if fmdata.is_valid():
            degree = fmdata.cleaned_data.get('degree')
            university = fmdata.cleaned_data.get('university')
            pass_out = fmdata.cleaned_data.get('pass_out')
            percentage = fmdata.cleaned_data.get('percentage')
            qualdata = Qualification.objects.create(profile_id=proid.id,degree=degree,pass_out=pass_out,percentage=percentage,university=university)
            qualdata.save()
            messages.success(request,'Academic detail inserted successfully ....!')
            return redirect('homepage')
        else:
            context={'forms':fmdata}
            return render(request,'qulificationadd.html',context)
        
    else:
        return redirect('homepage')
def getskills(request):
    email = request.session.get('email')
    if email :
        proid = Profile.get_profiles(email)
        data = TechnicalSkill.techskill(proid.id)
        if data :
            skills ={
                'database':data.database,
                'language': data.language,
                'framework': data.framework,
                'web_technology':data.web_technology,
            }
        else:
            skills= None
        context={'forms':TechnicalskillForm(initial=skills)}
        return render(request,'technicalupdate.html',context)
    else:
        return redirect('homepage')
def postskills(request):
    if request.method == "POST" and request.session.get('email') :
        email = request.session.get('email')
        proid = Profile.get_profiles(email)
        fmdata = TechnicalskillForm(request.POST)
        if fmdata.is_valid():
            db = fmdata.cleaned_data.get('database')
            framework = fmdata.cleaned_data.get('framework')
            lang = fmdata.cleaned_data.get('language')
            wb_tech = fmdata.cleaned_data.get('web_technology')
            tech_data = TechnicalSkill.objects.filter(profile_id=proid.id)
            update = tech_data.update(database=db,language=lang,framework=framework,web_technology=wb_tech)
            messages.success(request,'Your technical data is updated successfully...!')
            return redirect('homepage')
        else:
            context ={'forms':fmdata}
            messages.error(request,'Please fill required filled...!')
            return render(request,'technicalupdate.html',context)
    else:
        return redirect('homepage')
def getpersonalupdate(request):
    email = request.session.get('email')
    if email :
        proid = Profile.get_profiles(email)
        data=PersonalDetail.get_data(proid.id)
        if data :
            personals ={
                'father_name': data.father_name,
                'mother_name':data.mother_name,
                'permanent_address': data.permanent_address,
                'dob': data.dob,
                'language': data.language,
                'nationality': data.nationality,
                'hobby':data.hobby,
                'declare':data.declare
            }
        else:
            personals = None
        context ={'forms': PersonalDetailForm(initial=personals)}
        return render(request,'personalupdate.html',context)
    else:
        return redirect('homepage')
def postpersonalupdate(request):
    if request.method == 'POST' and request.session.get('email'):
        email = request.session.get('email')
        fmdata = PersonalDetailForm(request.POST)
        proid = Profile.get_profiles(email)
        if fmdata.is_valid():
            father_name = fmdata.cleaned_data.get('father_name')
            mother_name = fmdata.cleaned_data.get('mother_name')
            permanent_address = fmdata.cleaned_data.get('permanent_address')
            dob = fmdata.cleaned_data.get('dob')
            language =fmdata.cleaned_data.get('language')
            nationality =  fmdata.cleaned_data.get('nationality')
            hobby = fmdata.cleaned_data.get('hobby')
            declare = fmdata.cleaned_data.get('declare')
            res= PersonalDetail.objects.filter(profile_id=proid.id)
            res.update(father_name=father_name,mother_name=mother_name,permanent_address=permanent_address,dob=dob,language=language,nationality=nationality,hobby=hobby,declare=declare)
            messages.success(request,'Personal data updated successfully..!')
            return redirect('homepage')
        else:
            context={'forms':fmdata}
            messages.error(request,'Please eanter valid data..!')
            return render(request,'personalupdate.html',context)
    else:
        return redirect('homepage')
def getemail(request):
    context={'forms':EmailForm()}
    return render(request,'contactus.html',context)
def postemail(request):
    if request.method == 'POST':
        fmdata = EmailForm(request.POST)
        if fmdata.is_valid():
            sender = fmdata.cleaned_data.get('email')
            name = fmdata.cleaned_data.get('name')
            sub = fmdata.cleaned_data.get('subject')
            phone = fmdata.cleaned_data.get('phone')
            content = fmdata.cleaned_data.get('message')
            main_content="Hi, My name is "+name + "I want to "+ content
            send_mail(sub,main_content,'developerdjango03@gmail.com',[sender],fail_silently=False)
            messages.success(request,'Messages send successfully..!')
        else:
            context={'forms':fmdata}
            return render(request,'contactus.html',context)
    else:
        return redirect('homepage')
