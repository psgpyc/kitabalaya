from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from coreaccounts.models import ActivateEmail
User = get_user_model()


class UserAdmin(BaseUserAdmin):
    search_fields = ['email','full_name']
    ordering = ['id']
    list_display = ['email', 'full_name', 'is_active', 'is_staff', 'is_superuser']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            'Personal Info',
            {
                'fields':
                    (
                        'full_name',
                        'phone_number',
                        'gender',
                    )
            }
        ),
        (
            'Status',
            {
                'fields':
                    (
                        'is_confirmed',
                        'is_active',
                    )
            }
        ),
        (
            'permissions',
            {
                'fields':
                    (
                        'is_staff',
                        'is_superuser',
                        'user_permissions',
                    )
            }
        ),

        (
            'Dates',
            {
                'fields':
                    (
                        'last_login',
                    )
            }
        )


    )

    add_fieldsets = (
        (
            None,
            {
                'classes':
                    (
                        'wide',
                    ),
                'fields':
                    (
                        'email',
                        'full_name',
                        'phone_number',
                        'gender',
                        'password1',
                        'password2',
                    )
            }
        ),
    )


admin.site.register(User, UserAdmin)
admin.site.register(ActivateEmail)
