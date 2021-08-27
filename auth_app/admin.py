from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from auth_app.models import Account


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,             # original form fieldsets, expanded
        (
            'Custom User Model Fields',   # group heading
            {
                'fields': (               # added fields
                    'bio',
                    'profile_image',
                    'date_of_birth',
                    'followers',
                    'following',
                    'likes',
                    'dislikes',
                ),
            },
        ),
    )


admin.site.register(Account, CustomUserAdmin)
