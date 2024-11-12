from django import forms
from .models import User, Product, ProductImage
from django.contrib.auth.forms import AuthenticationForm

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'telefone', 'password']
        widgets = {
            'first_name': forms.EmailInput(attrs={'placeholder': 'Digite seu nome', 'class': 'form-control'}),
            'last_name': forms.EmailInput(attrs={'placeholder': 'Digite seu sobrenome', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Digite seu email', 'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Digite seu senha', 'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'placeholder': 'Digite seu telefone', 'class': 'form-control'}),
        }
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'Email',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['first_name'].required = True
        self.fields['last_name'].required = False
        self.fields['email'].required = True
        self.fields['telefone'].required = True
        self.fields['password'].required = True

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
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
        fields = ['first_name', 'last_name', 'email', 'telefone', 'endereco', 'foto_perfil']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sobrenome'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@exemplo.com'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'telefone'}),
            'endereco': forms.TextInput(attrs={'id': 'endereco', 'class': 'form-control', 'placeholder': 'Localização a partir do Cep.', 'readonly': 'readonly'}),
        }
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'Email',
            'telefone': 'Telefone',
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