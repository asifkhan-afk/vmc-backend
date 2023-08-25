from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Speciality)
admin.site.register(Education)
admin.site.register(DrProfile)
admin.site.register(WorkExperience)
class ResearchAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('id', 'title', 'doctor', 'is_active', 'posted_at', 'application_deadline')
    
    # Fields to use for searching in the admin panel
    search_fields = ('id', 'title', 'doctor__first_name', 'doctor__last_name')
    
    # Read-only fields in the admin detail view
    readonly_fields = ('is_active',)

admin.site.register(Research, ResearchAdmin)
admin.site.register(ResearchApply)