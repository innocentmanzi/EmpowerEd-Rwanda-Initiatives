from django.contrib import admin
from .models import User, Category

# @admin.register(Category)
# class CategoryModelAdmin(admin.ModelAdmin):
#     list_display = ('title', 'date')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'full_name', 'role', 'category', 'phone', 'is_admin', 'is_staff', 'is_active')
    list_display_links = ('username', 'email', 'full_name')
    search_fields = ('username', 'email', 'full_name', 'category')
    list_filter = ('is_admin', 'is_staff', 'is_active')

    # fieldsets = (
    #     (None, {"fields": ("email",)}),
    #     ("Booleans", {"fields": ("is_active", "is_staff", "is_admin")}),
    #     ("Timestamps", {"fields": ("date", "updated")}),
    # )

    readonly_fields = (
        "date",
        "updated",
    )

    ordering = ('-date',)
