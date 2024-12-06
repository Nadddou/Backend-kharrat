# urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from products.views import secret_key_login, csrf_token_view, ContactInfoViewSet, SocialMediaViewSet, ProductCategoryViewSet, RealisationViewSet, DevisDemandeViewSet, ContactMessageViewSet, ProductInfoViewSet, auth_status, logout_view  
from django.conf import settings
from django.conf.urls.static import static
from products import views
from django.contrib.auth import views as auth_views
from products import views as product_views


router = DefaultRouter()
router.register(r'categories', ProductCategoryViewSet)
router.register(r'realisations', RealisationViewSet)
router.register(r'devis-demandes', DevisDemandeViewSet)
router.register(r'contact-form', ContactMessageViewSet)
router.register(r'product-info', ProductInfoViewSet) 
router.register(r'contact-info', ContactInfoViewSet, basename='contact-info')
router.register(r'social-media', SocialMediaViewSet, basename='social-media')


urlpatterns = [
    path('secretkey', secret_key_login, name='secret_key_login'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/search/', views.search, name='search'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/auth-status/', auth_status, name='auth_status'), 
    path('api/csrf-token/', csrf_token_view, name='csrf_token'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/list-contact-info/', views.list_contact_info, name='list_contact_info'),
    path('api/update-general-info/<int:pk>/', views.update_general_info, name='update_general_info'),
    path('api/update-social-link/<int:pk>/', views.update_social_link, name='update_social_link'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('accounts/logout/', logout_view, name='logout'),
    
    # Superuser-only URLs for user management
    # API Endpoints
    path('api/manage-users/', product_views.api_list_users, name='api_manage_users'),
    path('api/manage-users/add/', product_views.api_add_user, name='api_add_user'),
    path('api/manage-users/edit/<int:pk>/', product_views.api_edit_user, name='api_edit_user'),
    path('api/manage-users/delete/<int:pk>/', product_views.api_delete_user, name='api_delete_user'),

    # HTML Views for template rendering
    path('dashboard/manage-users/', product_views.manage_users, name='manage_users'),
    path('dashboard/manage-users/add/', product_views.add_user, name='add_user'),
    path('dashboard/manage-users/<int:pk>/edit/', product_views.edit_user, name='edit_user'),
    path('dashboard/manage-users/<int:pk>/delete/', product_views.delete_user, name='delete_user'),


    # URLs for ProductInfo
    path('dashboard/product-info/', product_views.productinfo_list, name='productinfo_list'),
    path('dashboard/product-info/add/', product_views.productinfo_create, name='productinfo_create'),
    path('dashboard/product-info/<int:pk>/edit/', product_views.productinfo_update, name='productinfo_update'),
    path('dashboard/product-info/<int:pk>/delete/', product_views.productinfo_delete, name='productinfo_delete'),


    # Shared URLs for ProductCategory
    path('dashboard/product-categories/', product_views.productcategory_list, name='productcategory_list'),
    path('dashboard/product-categories/add/', product_views.productcategory_create, name='productcategory_create'),
    path('dashboard/product-categories/<int:pk>/edit/', product_views.productcategory_update, name='productcategory_update'),
    path('dashboard/product-categories/<int:pk>/delete/', product_views.productcategory_delete, name='productcategory_delete'),

    # Shared URLs for Realisation
    path('dashboard/realisations/', product_views.realisation_list, name='realisation_list'),
    path('dashboard/realisations/add/', product_views.realisation_create, name='realisation_create'),
    path('dashboard/realisations/edit/<int:pk>/', product_views.realisation_update, name='realisation_update'),
    path('dashboard/realisations/<int:pk>/delete/', product_views.realisation_delete, name='realisation_delete'),

    # Shared URLs for DevisDemande
    path('dashboard/devis-demandes/', product_views.devisdemande_list, name='devisdemande_list'),
    path('dashboard/devis-demandes/<int:pk>/', product_views.devisdemande_detail, name='devisdemande_detail'),
    # path('dashboard/devis-demandes/<int:pk>/update-status/', product_views.devisdemande_update_status, name='devisdemande_update_status'),
    path('dashboard/devis-demandes/<int:pk>/delete/', product_views.devisdemande_delete, name='devisdemande_delete'),
    path('dashboard/devis-demandes/<int:pk>/update-status/', views.test_devisdemande_update_status, name='test_devisdemande_update_status'),

    # Shared URLs for ContactMessage
    path('dashboard/contact-messages/', product_views.contactmessage_list, name='contactmessage_list'),
    path('dashboard/contact-messages/<int:pk>/', product_views.contactmessage_detail, name='contactmessage_detail'),
    path('dashboard/contact-messages/<int:pk>/delete/', product_views.contactmessage_delete, name='contactmessage_delete'),
    path('dashboard/contact-messages/<int:pk>/update-status/', views.test_contactmessage_update_status, name='contactmessage_delete'),
]   
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
