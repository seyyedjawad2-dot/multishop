
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm,UserChangeForm
from .models import User,  EmailOTP


class UserAdmin(BaseUserAdmin):
   form=UserChangeForm
   add_form=UserCreationForm
   list_display=("email","is_admin")
   list_filter=["is_admin"]
   fieldsets=[(None,{"fields":["email","password"]}),("Personal info",{"fields":["fullname"]}),("Permissions",{"fields":["is_admin"]}),]
# add_fieldsets is not a standard ModelAdmin attribute. UserAdmin# overrides get_fieldsets to use this attribute when creating a user.
   add_fieldsets=[(None,{"classes":["wide"],"fields":["email","fullname","password1","password2"],},),]
   search_fields=["email"]
   ordering=["email"]
   filter_horizontal=()# Now register the new UserAdmin...
   admin.site.register(User)
   admin.site.unregister(Group)
   admin.site.register(EmailOTP)