from django.contrib import admin		

from djoptimizely.models import OptimizelyDataFile


class OptimizelyDataFileAdmin(admin.ModelAdmin):		
    list_display = ('environment', 'current_revision', 'updated_at',)			

admin.site.register(OptimizelyDataFile, OptimizelyDataFileAdmin) 
