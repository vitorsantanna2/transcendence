# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import UserPong


# class UserPongAdmin(UserAdmin):
#     model = UserPong
#     list_display = (
#         "id",
#         "username",
#         "email",
#         "name",
#         "phoneNumber",
#     )
#     list_filter = ("is_staff", "is_superuser", "is_active")
#     search_fields = ("username", "email", "name")
#     ordering = ("id",)
#     fieldsets = (
#         (None, {"fields": ("username", "password")}),
#         ("Personal Info", {"fields": ("name", "email", "phoneNumber")}),
#         ("Permissions", {"fields": ("is_staff", "is_superuser", "is_active")}),
#         ("Timestamps", {"fields": ("created_at", "updated_at")}),
#     )
#     add_fieldsets = (
#         (
#             None,
#             {
#                 "classes": ("wide",),
#                 "fields": (
#                     "username",
#                     "email",
#                     "name",
#                     "password1",
#                     "password2",
#                 ),
#             },
#         ),
#     )


# admin.site.register(UserPong, UserPongAdmin)
