from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Defina uma classe personalizada para estender o UserAdmin
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')

# Desregistre o UserAdmin padrão
admin.site.unregister(User)

# Registre o UserAdmin personalizado
admin.site.register(User, CustomUserAdmin)
