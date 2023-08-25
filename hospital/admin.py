from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(HospitalProfile)
class JobAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('id', 'hospital', 'position','job_type','workplace','description','qualification','requirements','start_salary','end_salary','published_at', 'is_active',  'application_deadline')
    
    # Fields to use for searching in the admin panel
    search_fields = ('id', 'title', 'hospital__first_name')
    
    # Read-only fields in the admin detail view
    readonly_fields = ('is_active',)

admin.site.register(Job, JobAdmin)
admin.site.register(HospitalDepartment)

admin.site.register(Gallery)
admin.site.register(HospitalServices)

admin.site.register(Affiliated_doctors)
admin.site.register(Apply)

