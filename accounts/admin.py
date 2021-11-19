from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User as MyUser, Profile, Relation
from .forms import UserCreationForm, UserChangeForm


class ProfileInline(admin.StackedInline):
    model = Profile
    fields = ('user', 'full_name', 'age', 'image', 'bio')


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'email', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )

    search_fields = ('username', 'email')
    ordering = ('username', 'email',)
    filter_horizontal = ()
    inlines = (ProfileInline,)


admin.site.register(MyUser, UserAdmin)
admin.site.register(Profile)
admin.site.unregister(Group)
admin.site.register(Relation)