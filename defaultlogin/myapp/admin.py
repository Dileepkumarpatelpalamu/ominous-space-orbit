from django.contrib import admin
from myapp.models import *
# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id','name','title','phone','email']

@admin.register(PersonalDetail)
class PersonalDetailAdmin(admin.ModelAdmin):
    list_display = ['father_name','mother_name','dob','language','hobby']

@admin.register(Qualification)
class QualificationDetailAdmin(admin.ModelAdmin):
    list_display = ['degree','university','pass_out','percentage']

@admin.register(TechnicalSkill)
class TechnicalSkillAdmin(admin.ModelAdmin):
    list_display = ['database','language','framework','web_technology']

@admin.register(PasswordData)
class PasswordAdmin(admin.ModelAdmin):
    list_display = ['profile','linkin','git_link','wb_link','password']
