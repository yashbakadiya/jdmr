from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, OTPModel

# Register your models here.
@admin.register(User)
class UsersAdmin(UserAdmin):
    list_display = ('id', 'full_name', 'email', 'user_type', 'institution', 'is_active')
    search_fields = ('email', 'full_name',)
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('-id',)
    filter_horizontal = ()
    list_filter = ('institution','user_type',)
    fieldsets = ()

@admin.register(OTPModel)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'otp', 'timestamp')
