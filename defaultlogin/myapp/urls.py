from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('',views.homepage,name="homepage"),
    path('login/',views.userlogin,name="login"),
    path('userloginpost/',views.userloginpost,name='userloginpost'),
    path('signup/',views.usersignup,name="signup"),
    path('usersignuppost/',views.usersignuppost,name="usersignuppost"),
    path('getprofileupdate/',views.getprofileupdate,name='getprofileupdate'),
    path('postprofileupdate/',views.postprofileupdate,name='postprofileupdate'),
    path('getsocialupdate/',views.getsocialupdate,name="getsocialupdate"),
    path('postsocialupdate/',views.postsocialupdate,name='postsocialupdate'),
    path('getqulificationupdate/',views.getqulificationupdate,name='getqulificationupdate'),
    path('postqulificationupdate/',views.postqulificationupdate,name='postqulificationupdate'),
    path('getskillsupdate/',views.getskills,name='getskillsupdate'),
    path('postskillsupdate/',views.postskills,name='postskillupdate'),
    path('getpersonalupdate/',views.getpersonalupdate,name='getpersonalupdate'),
    path('postpersonalupdate/',views.postpersonalupdate,name='postpersonalupdate'),
    path('getemail/',views.getemail,name='getemail'),
    path('postemail/',views.postemail,name='postemail'),
    path('userlogout/',views.userlogout,name="userlogout"),
    path('admin/', admin.site.urls),
]
#urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
