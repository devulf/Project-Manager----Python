from projects.models import Project

from django.contrib import admin


class ProjectAdmin(admin.ModelAdmin):
    # ...
    list_display = ('name',  'description', 'start_date', 'end_date')
    list_filter = ['name']
    search_fields = ['name']
    date_hierarchy = 'start_date'


admin.site.register(Project, ProjectAdmin)
