from django.contrib.auth import login, logout
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views import View
from django.urls import reverse_lazy
from .models import Profile, Product, ProductImage
from . import forms

class IndexListView(ListView):
    model = Product
    template_name = 'pages/index.html'
    context_object_name = 'products' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for product in context['products']:
            if product.condition == 'Novo':
                product.badge = 'badge-success'
            elif product.condition == 'Usado':
                product.badge = 'badge-warning'
            elif product.condition == 'Semi-novo':
                product.badge = 'badge-info'
            elif product.condition == 'Recondicionado':
                product.badge = 'badge-primary'
            elif product.condition == 'Danificado':
                product.badge = 'badge-danger'
            else:
                product.badge = 'badge-secondary'

            address = product.usuario.profile.endereco.split(", ")
            product.city = address[1] if len(address) > 1 else product.usuario.profile.endereco
        return context

    def get_queryset(self):
        return Product.objects.prefetch_related('images').all()
    
class ProductDetailView(DetailView):
    model = Product
    template_name = 'pages/product/detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.prefetch_related('images')
    
class RegisterCreateView(CreateView):
    template_name = 'pages/authentication/register.html'
    form_class = forms.RegistrationForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)
    
class LoginView(LoginView):
    authentication_form = forms.AuthenticateForm
    template_name = 'pages/authentication/login.html'
        
class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('index')


class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'pages/profile/profile.html'
    success_url = reverse_lazy('profile')
    success_message = 'Perfil atualizado com sucesso!'

    def get(self, request, *args, **kwargs):
        user_form = forms.UserProfileForm(instance=request.user)
        profile_form = forms.ProfileForm(instance=request.user.profile)
        return render(request, self.template_name, {'user_form': user_form, 'profile_form': profile_form})

    def post(self, request, *args, **kwargs):
        user_form = forms.UserProfileForm(request.POST, instance=request.user)
        profile_form = forms.ProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return self.form_valid(user_form)

        return self.render_to_response({'user_form': user_form, 'profile_form': profile_form})

    def form_valid(self, form):
        return super().form_valid(form)

    def form_valid(self, user_form):
        return super().form_valid(user_form)

    def form_invalid(self, user_form, profile_form):
        return self.render_to_response(self.get_context_data(user_form=user_form, profile_form=profile_form))

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
        profile = get_object_or_404(Profile, user=self.request.user)
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
        profile = get_object_or_404(Profile, user=self.request.user)
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