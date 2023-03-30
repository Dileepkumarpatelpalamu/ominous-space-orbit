from django import forms
from django.db.models import fields
from django.forms import widgets
from django.forms.widgets import TextInput
from .models import *
from django.core.exceptions import ValidationError
import re
class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not Profile.objects.filter(email=email).count():
            raise ValidationError("Entered email not registered !")
        return email
    def clean_password(self):
        pattern = "[A-Z]+[a-z]+[0-9]+"
        password = self.cleaned_data.get('password')
        if not re.search(pattern,password):
            raise ValidationError("Password contain at least a upper case, lower case and  digits !")
        return password

class SignupForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Phone number'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm password'}))
    def clean_name(self):
        name = self.cleaned_data.get('name')
        names = [item for item in name.split() if item.isalpha()]
        if len(names) != len(name.split()):
            raise ValidationError("Please enter only letters!")
        return name
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Profile.objects.filter(email=email).count():
            raise ValidationError('Email already exits try another or login!')
        return email
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit():
            raise ValidationError('Enter only digits!')
        elif len(phone)!=10:
            raise ValidationError('Phone number only 10 digits allowed! ')
        return phone
    def clean_password(self):
        password = self.cleaned_data.get('password')
        pattern = "[A-Z]+[a-z]+[0-9]+"
        if not re.search(pattern,password):
            raise ValidationError('Password must contains upper case, lower case and one digits!')
        return password
    def clean_confirm_password(self):
        confirm = self.cleaned_data.get('confirm_password')
        password = self.cleaned_data.get('password')
        if password != confirm:
            raise ValidationError("Password and confirm password not matched!")
        return confirm

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields =['name','title','phone','career','photo']
        labels={
            'name':'Name',
            'title':'Title',
            'career':'Careers and Objectives',
            'photo':'Select photo to upload',
            }
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Full name !'}),
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Title !'}),
            'phone':forms.TextInput(attrs={'class':'form-control','placeholder':'Phone number !'}),
            'career':forms.Textarea(attrs={'class':'form-control','placeholder':'Describe careers and objective in details !'}),
        }
    def clean_name(self):
        name = self.cleaned_data.get('name')
        names = [item for item in name.split() if item.isalpha()]
        if len(names) != len(name.split()):
            raise ValidationError("Please enter only letters!")
        return name
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) ==0:
            raise ValidationError('Title must be fill!')
        elif len(title)<5:
            raise ValidationError('Title muste be 5 or more letters!')
        return title
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit():
            raise ValidationError('Enter only digits!')
        elif len(phone)!=10:
            raise ValidationError('Phone number only 10 digits allowed! ')
        return phone
    def clean_career(self):
        career = self.cleaned_data.get('career')
        if not len(career):
            raise ValidationError('Careers and ojective fields can not be blank!')
        elif not len(career)>=20:
            raise ValidationError('Careers and objective must be 20 characters!')
        return career

class SocialUpdateForm(forms.ModelForm):
    class Meta:
        model = PasswordData
        fields =['linkin','git_link','wb_link']
        labels={
            'linkin': 'Linkedin',
            'git_link':'Github account',
            'wb_link': 'Website link',
        }
        widgets={
            'linkin':forms.URLInput(attrs={'class':'form-control','placeholder':'linkedin id'}),
            'git_link':forms.URLInput(attrs={'class':'form-control','placeholder':'Github account'}),
            'wb_link':forms.URLInput(attrs={'class':'form-control','placeholder':'Website link'}),
        }

class QulificationForm(forms.ModelForm):
    class Meta:
        model = Qualification
        fields = ['degree','university','pass_out','percentage']
        labels = {
            'degree':'Degree',
            'university':'University',
            'pass_out': 'Passing years',
            'percentage':'Percentage',
        }
        widgets={
            'degree':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter degree'}),
            'university':forms.TextInput(attrs={'class':'form-control','placeholder':'University name'}),
            'pass_out':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter passing year'}),
            'percentage':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter percentage'}),
        }

class TechnicalskillForm(forms.ModelForm):
    class Meta:
        model = TechnicalSkill
        fields = ['database','language','framework','web_technology']
        labels = {
            'database':'Databases',
            'language':'Programming languages',
            'framework':'Frameworks',
            'web_technology':'Web designing tools',
        }
        widgets={
            'database': forms.TextInput(attrs={'class':'form-control','placeholder':'Databases'}),
            'language': forms.TextInput(attrs={'class':'form-control','placeholder':'Programming languages'}),
            'framework': forms.TextInput(attrs={'class':'form-control','placeholder':'Framework names'}),
            'web_technology': forms.TextInput(attrs={'class':'form-control','placeholder':'Web designing tools'}),
        }
class PersonalDetailForm(forms.ModelForm):
    class Meta:
        model = PersonalDetail
        fields =['father_name','mother_name','permanent_address','dob','language','nationality','hobby','declare']
        labels= {
            'father_name':'Father s name ',
            'mother_name' : 'Mother s name',
            'permanent_address': 'Permanent address',
            'dob': 'Date of birth',
            'language':'Languages known',
            'nationality':'Nationality',
            'hobby': 'Hobbies',
            'declare':'Declarations',
        }
        widgets={
            'father_name': forms.TextInput(attrs={'class':'form-control','placeholder':'Father name'}),
            'mother_name': forms.TextInput(attrs={'class':'form-control','placeholder':'Mother name'}),
            'permanent_address': forms.TextInput(attrs={'class':'form-control','placeholder':'Permanent address'}),
            'dob': forms.DateInput(attrs={'class':'form-control'}),
            'language': forms.TextInput(attrs={'class':'form-control','placeholder':'Known lanugages'}),
            'nationality': forms.TextInput(attrs={'class':'form-control','placeholder':'Nationality'}),
            'hobby': forms.TextInput(attrs={'class':'form-control','placeholder':'Hobbies'}),
            'declare': forms.Textarea(attrs={'class':'form-control','placeholder':'Declare'}),
        }

class EmailForm(forms.Form):
    name = forms.CharField(label='Name',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name'}))
    subject = forms.CharField(label='Subject',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your subjects..'}))
    email = forms.CharField(label='Email',widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email..'}))
    phone = forms.CharField(label='Name',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Mobile number ...'}))
    message = forms.CharField(label='Name',widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Messages here ...'}))
    


        
