from django.contrib import admin
from .models import ProductCategory, Realisation, DevisDemande, ContactMessage, ProductInfo, GeneralContactInfo, SocialMediaLink

admin.site.register(ProductCategory)
admin.site.register(Realisation)
admin.site.register(DevisDemande)
admin.site.register(ContactMessage)
admin.site.register(ProductInfo)
admin.site.register(GeneralContactInfo)
admin.site.register(SocialMediaLink)

