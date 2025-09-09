from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile

# Define un 'inline' para el modelo Profile.
# Esto permite que el Profile se muestre y se edite dentro de la página del User.
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Perfiles'

# Define un nuevo User admin que incluye el ProfileInline
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

# Vuelve a registrar el modelo User de Django para usar nuestro UserAdmin personalizado
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

