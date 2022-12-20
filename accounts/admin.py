from django.contrib import admin
from .models import Profile, Log
# Register your models here.
from django.utils.safestring import mark_safe
from django.contrib import messages
# Register your models here.

class LogAdmin(admin.ModelAdmin):
    list_display = ["created_at"]

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = ('user','first_name', 'last_name', 'job')
    search_fields = ('first_name', 'last_name', 'job')
    list_display_links = ('user','first_name', 'last_name', 'job')
    sortable_by = ('first_name', 'last_name', 'job')
    readonly_fields = ('show_image','slug')



    def show_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" alt="{obj.first_name}" width="100" height="100">'.format(
            url = obj.image.url,
            width=obj.image.width,
            height=obj.image.height,
            )
    )
    show_image.short_description = "نمایش عکس"



admin.site.register(Log, LogAdmin)