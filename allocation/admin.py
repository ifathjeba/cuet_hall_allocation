from django.contrib import admin
from .models import Profile, Hall, RoomApplication

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Hall)
admin.site.register(RoomApplication)
