from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile, Product, ProductImage

class RegistrationForm(forms.ModelForm):
    telefone = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu telefone'
        }),
        required=True
    )

    first_name = forms.CharField(
        label='Nome',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu nome' 
        })
    )

    last_name = forms.CharField(
        label='Sobrenome',
        required=False, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu sobrenome'
        })
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu email'
        })
    )

    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua senha'
        })
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            Profile.objects.create(user=user, telefone=self.cleaned_data['telefone'])
        return user


class AuthenticateForm(AuthenticationForm):
    username = forms.CharField(
        label='Email', 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu email'
        })
    )
    
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua senha'
        })
    )

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sobrenome'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@exemplo.com'}),
        }
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'Email',
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['telefone', 'endereco', 'foto_perfil']
        widgets = {
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'telefone'}),
            'endereco': forms.TextInput(attrs={'id': 'endereco', 'class': 'form-control', 'placeholder': 'Localização a partir do Cep.', 'readonly': 'readonly'}),
        }
        labels = {
            'endereco': 'Endereço',
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'condition', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Roupas, Móveis, Eletrodomésticos', 'required': True}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': '4', 'placeholder': 'Detalhes sobre o item que está doando', 'required': True}),
            'condition': forms.Select(attrs={'required': True}),
            'category': forms.Select(attrs={'required': True}),
        }
        labels = {
            'name': 'Nome do item',
            'description': 'Descrição',
            'condition': 'Condição do item',
            'category': 'Categoria',
        }

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']

ProductImageFormSet = forms.modelformset_factory(ProductImage, form=ProductImageForm, extra=5)