from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
     path('', views.IndexListView.as_view(), name='index'), 
     path('produto/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
     path('register/', views.RegisterCreateView.as_view(), name='register'),
     path('login/', views.LoginView.as_view(), name='login'),
     path('logout/', views.LogoutView.as_view(), name='logout'),
     path('perfil/', views.ProfileUpdateView.as_view(), name='profile'),
     path('produtos/', views.ProductListView.as_view(), name='product'),
     path('produtos/add/', views.ProductCreateView.as_view(), name='product_add'),
     path('produtos/edit/<int:pk>/', views.ProductUpdateView.as_view(), name='product_edit'),
     path('produtos/delete/<int:pk>/', views.ProductDeleteView.as_view(), name='product_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)