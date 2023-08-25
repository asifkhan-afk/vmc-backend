from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User

# admin.site.register(User, UserAdmin)
# class AdminUserModel(UserAdmin):
    
    # list_filter=('is_admin','is_student')
    # fieldsets = (
    #     ('User Credentials' , {'fields':('email','password')}),
    #     ('Personal info',{'fields': ('name','is_admin')}),
    #     ('Permissions',{'fields':('is_doctor',)}),
    # )
    # add_fieldsets=(
    #     (None,{
    #         'classes':('wide',),
    #         'fields':('email','name','is_admin','is_student','is_doctor','password1','password2'),
    #     }),
    # )
    # search_fields=('email',)
    # ordering=('email',)
    # filter_horizontal=()
admin.site.register(User)
# admin.site.register(Appointment)
