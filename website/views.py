from django.contrib.auth import login, logout
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.views import View
from django.urls import reverse_lazy
from django.db.models import Q
from .models import User, Product, ProductImage
from . import forms

class BadgeMixin:
    def add_badges(self, products):
        for product in products:
            product.badge = self.get_badge(product.condition)

    def get_badge(self, condition):
        if condition == 'Novo':
            return 'badge-success'
        elif condition == 'Usado':
            return 'badge-warning'
        elif condition == 'Semi-novo':
            return 'badge-info'
        elif condition == 'Recondicionado':
            return 'badge-primary'
        elif condition == 'Danificado':
            return 'badge-danger'
        else:
            return 'badge-secondary'

class IndexListView(BadgeMixin, ListView):
    model = Product
    template_name = 'pages/index.html'
    context_object_name = 'products' 

    def get_queryset(self):
        return Product.objects.prefetch_related('images').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = context['products']
        for product in products:
            address = product.usuario.endereco.split(", ")
            product.city = address[1] if len(address) > 1 else product.usuario.endereco
        self.add_badges(products)
        return context

class SearchView(BadgeMixin, TemplateView):
    template_name = 'pages/search_results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        
        if query:
            products = Product.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
            users = User.objects.filter(
                Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(endereco__icontains=query)
            )
        else:
            products = Product.objects.none()
            users = User.objects.none()

        context['query'] = query
        context['products'] = products
        for product in context['products']:
            address = product.usuario.endereco.split(", ")
            product.city = address[1] if len(address) > 1 else product.usuario.endereco
        context['users'] = users
        self.add_badges(products)
        return context

class ProductDetailView(BadgeMixin, DetailView):
    model = Product
    template_name = 'pages/product/detail.html'

    def get_queryset(self):
        return Product.objects.prefetch_related('images')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = context['product']
        self.add_badges([product])
        return context

class RegisterCreateView(CreateView):
    template_name = 'pages/authentication/register.html'
    form_class = forms.RegistrationForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)

class LoginView(LoginView, SuccessMessageMixin):
    authentication_form = forms.AuthenticateForm
    template_name = 'pages/authentication/login.html'
    success_message = 'Logado com sucesso!'

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, self.success_message)
        return super().form_valid(form)

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('index')

class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'pages/profile/profile.html'
    success_url = reverse_lazy('profile')
    success_message = 'Perfil atualizado com sucesso!'
    form_class = forms.UserProfileForm

    def get_object(self):
        return self.request.user

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'pages/product/list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(usuario=self.request.user).prefetch_related('images')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['has_products'] = Product.objects.filter(usuario=self.request.user).exists()
        return context
    
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = forms.ProductForm
    template_name = 'pages/product/add.html'
    success_url = reverse_lazy('product')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(User, id=self.request.user.id)
        context['location'] = profile.endereco
        return context

    def form_valid(self, form):
        product = form.save(commit=False)
        product.usuario = self.request.user
        product.save()

        images = self.request.FILES.getlist('images') 
        for image in images:
            ProductImage.objects.create(product=product, image=image)

        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = forms.ProductForm
    template_name = 'pages/product/edit.html'
    success_url = reverse_lazy('product')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(User, id=self.request.user.id)
        context['product_images'] = self.object.images.all()
        context['location'] = profile.endereco
        return context


    def get_queryset(self):
        return Product.objects.filter(usuario=self.request.user)

    def form_valid(self, form):
        product = form.save(commit=False)
        
        remove_images = self.request.POST.getlist('remove_images')
        for image_id in remove_images:
            try:
                image = ProductImage.objects.get(id=image_id)
                image.delete() 
            except Image.DoesNotExist:
                pass 
        product.save()

        images = self.request.FILES.getlist('images')
        for image in images:
            ProductImage.objects.create(product=self.object, image=image)

        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'pages/product/delete.html'
    success_url = reverse_lazy('product')

    def get_queryset(self):
        return Product.objects.filter(usuario=self.request.user)