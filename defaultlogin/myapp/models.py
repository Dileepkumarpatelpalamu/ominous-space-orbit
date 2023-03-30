from django.db import models

# Create your models here.
from django.db import models
from django.db.models.fields import CharField

# Create your models here.

class Profile(models.Model):
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=50,blank=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    career = models.TextField( blank=True)
    photo = models.ImageField(upload_to='',blank=True)
    date = models.DateField()
    def __str__(self):
        return "%s %s %s"%(self.name,self.email,self.title)
    @staticmethod
    def get_profiles(email=None):
        if not email:
            return Profile.objects.all().first()
        else:
            return Profile.objects.get(email=email)
    @staticmethod
    def get_login(email):
        user = Profile.objects.filter(email=email).first()
        if user :
            return user
        return None

class PasswordData(models.Model):
    profile = models.OneToOneField(Profile,on_delete=models.CASCADE)
    password = models.CharField(max_length=500)
    linkin = models.URLField(blank=True)
    git_link = models.URLField(blank=True)
    wb_link = models.URLField(blank=True)
    def __str__(self):
        return "%s"%(self.password)
    @staticmethod
    def get_password(id):
        userpass = PasswordData.objects.filter(profile_id=id).first()
        if userpass:
            return userpass
        return None
    @staticmethod
    def get_link(id):
        return PasswordData.objects.filter(profile_id=id).first()
         
class PersonalDetail(models.Model):
    profile = models.OneToOneField(Profile,on_delete=models.CASCADE)
    father_name = models.CharField(max_length=50)
    mother_name = models.CharField(max_length=50)
    permanent_address = models.TextField()
    dob = models.DateField()
    language = models.CharField(max_length=100)
    nationality = models.CharField(max_length=50)
    hobby = models.CharField(max_length=100)
    declare = models.TextField()
    def __str__(self):
        return "%s %s"%(self.language,self.dob)
    @staticmethod
    def get_data(id):
        return PersonalDetail.objects.filter(profile_id=id).last()

class Qualification(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    degree = models.CharField(max_length=100)
    university = models.CharField(max_length=100)
    pass_out = models.CharField(max_length=20)
    percentage = models.DecimalField(max_digits=5,decimal_places=3)
    def __str__(self):
        return "%s %s %s %s"%(self.degree,self.university,self.pass_out,self.percentage)
    @staticmethod
    def get_qualification(id):
        return Qualification.objects.filter(profile_id=id).order_by('-pass_out')

class TechnicalSkill(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    database = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    framework = models.CharField(max_length=100)
    web_technology = models.CharField(max_length=100)
    def __str__(self):
        return "%s %s %s %s"%(self.database,self.language,self.framework,self.web_technology)
    @staticmethod
    def techskill(id):
        return TechnicalSkill.objects.filter(profile__id=id).last()



