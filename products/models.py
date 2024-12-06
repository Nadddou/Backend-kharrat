from django.db import models
from django.contrib.auth.models import User
from django.db import models

User.add_to_class('secret_key', models.CharField(max_length=50, default="defaultkey"))

# ProductCategory model 
class ProductCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
    
# ProductInfo model 
class ProductInfo(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name="produits")
    name = models.CharField(max_length=255)
    description = models.TextField()
    images = models.ImageField(upload_to='produits/')

    def __str__(self):
        return self.name


# Realisation model for company projects
class Realisation(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name="realisations")
    name = models.CharField(max_length=255)
    description = models.TextField()
    customer_feedback = models.TextField(blank=True, null=True)
    images = models.ImageField(upload_to='realisations/')
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name




# DevisDemande model for quote requests sent by users
class DevisDemande(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=8, default="00000000")
    governorate = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(null=True)
    picture = models.ImageField(upload_to='devis_pictures/', blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    customer_contacted = models.BooleanField(default=False)
    request_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Devis Request from {self.name} on {self.submitted_at}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=8, default="00000000")
    subject = models.CharField(max_length=255)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    customer_contacted = models.BooleanField(default=False)
    request_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.name} on {self.submitted_at}"






class GeneralContactInfo(models.Model):
    TYPE_CHOICES = [
        ('email', 'Email'),
        ('phone', 'Téléphone'),
        ('address', 'Adresse'),
    ]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    value = models.TextField()  # Store email, phone number, or address
    label = models.CharField(max_length=100, blank=True, null=True)  # For more descriptive info (optional)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_type_display()}: {self.value}"


class SocialMediaLink(models.Model):
    platform = models.CharField(max_length=50)  # e.g., "Facebook", "Instagram"
    url = models.URLField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.platform}: {self.url}"




