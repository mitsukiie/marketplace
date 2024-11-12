from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Definindo a classe de administração do modelo CustomUser
class UserAdmin(UserAdmin):
    # Definindo os campos a serem exibidos na lista
    list_display = ('email', 'username', 'first_name', 'last_name', 'foto_perfil', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    
    # Definindo os campos que serão usados para criar um novo usuário
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )

    # Definindo os campos para edição do usuário
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações pessoais', {'fields': ('first_name', 'last_name')}),
        ('Informações extras', {'fields': ('telefone', 'endereco')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Especificando o campo de pesquisa
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)  # Ordena por email

# Registrando o modelo CustomUser e a classe de administração CustomUserAdmin
admin.site.register(User, UserAdmin)
