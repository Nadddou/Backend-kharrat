# serializers.py
from rest_framework import serializers
from .models import ProductCategory, Realisation, DevisDemande, ContactMessage, ProductInfo, GeneralContactInfo, SocialMediaLink


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductInfoSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductCategory.objects.all(),
        source='category',  # Connects to `category` field in the model
        write_only=True
    )
    category = ProductCategorySerializer(read_only=True)  # For read-only access to full category details
    images_url = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = ProductInfo
        fields = ['id', 'category', 'category_id', 'name', 'description', 'images', 'images_url']

    def get_images_url(self, obj):
        request = self.context.get('request')
        if obj.images:
            return request.build_absolute_uri(obj.images.url)
        return None  # Return None if no image is available

    def create(self, validated_data):
        category = validated_data.pop('category')
        validated_data['category'] = category
        return ProductInfo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        category = validated_data.pop('category', None)
        if category:
            instance.category = category

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if 'images' in self.initial_data and validated_data.get('images') is None:
            validated_data['images'] = instance.images

        instance.save()
        return instance


class RealisationSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductCategory.objects.all(),
        source='category',  # Assign to the `category` field in the model
        write_only=True
    )
    category = ProductCategorySerializer(read_only=True)  # Detailed category info for read
    images_url = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Realisation
        fields = ['id', 'category', 'category_id', 'name', 'description', 'customer_feedback', 'images', 'images_url', 'created_at']
    def get_images_url(self, obj):
        request = self.context.get('request')
        if obj.images:
            return request.build_absolute_uri(obj.images.url)
        return None  # Return None if no image is available

    def create(self, validated_data):
        category = validated_data.pop('category')
        validated_data['category'] = category
        return Realisation.objects.create(**validated_data)

    def update(self, instance, validated_data):
        category = validated_data.pop('category', None)
        if category:
            instance.category = category
        
        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Check if images are provided, else retain existing
        if 'images' in self.initial_data and validated_data.get('images') is None:
            validated_data['images'] = instance.images  # Retain existing if no new image provided

        instance.save()
        return instance




class DevisDemandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DevisDemande
        fields = [
            'id', 'name', 'email', 'phone', 'governorate', 'city', 
            'address', 'picture', 'submitted_at', 'customer_contacted', 
            'request_completed'
        ]
class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = [
            'id', 'name', 'email', 'phone', 'subject', 'message', 
             'submitted_at', 'customer_contacted', 
            'request_completed'
        ]



class GeneralContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralContactInfo
        fields = '__all__'


class SocialMediaLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaLink
        fields = '__all__'