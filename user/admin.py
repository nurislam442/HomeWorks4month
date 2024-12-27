from django.contrib import admin
from user.models import Profile
# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "age", "image")
    search_fields = ("user",)