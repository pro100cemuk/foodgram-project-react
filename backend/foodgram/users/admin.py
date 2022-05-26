from django.contrib import admin

from users.models import Follow, User


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name',)
    search_fields = ('username',)
    list_filter = ('email',)
    list_per_page = 10


admin.site.register(Follow)
