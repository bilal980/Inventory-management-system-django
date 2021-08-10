from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser
from .forms import MyUserChangeForm, MyUserCreationForm
from django.utils.translation import ugettext_lazy as _
# Register your models here.


class MyUserAdmin(UserAdmin):
    add_form = MyUserCreationForm
    form = MyUserChangeForm
    model = MyUser

    fieldsets = (
        (None, {'fields': ('email', 'password','date_joined','picture',)}),
        
        (_('Permissions'), {
            'fields': ('is_active','is_admin','is_staff', 'is_superuser', 'groups', 'user_permissions',),
        }),
        
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2','picture',),
        }),
    )
    list_display=('email',)
    ordering=('email',)
admin.site.register(MyUser, MyUserAdmin)
