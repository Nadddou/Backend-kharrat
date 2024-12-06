# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .models import ProductCategory, Realisation, DevisDemande, ContactMessage
from .serializers import ProductCategorySerializer, RealisationSerializer, DevisDemandeSerializer, ContactMessageSerializer, ProductInfoSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ProductCategory, Realisation, DevisDemande, ContactMessage, ProductInfo
from .forms import ProductCategoryForm, RealisationForm, DevisDemandeForm, ContactMessageForm, ProductInfoForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import logout, authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated , AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Realisation
from .serializers import RealisationSerializer
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import difflib
from .models import GeneralContactInfo, SocialMediaLink
from .serializers import GeneralContactInfoSerializer, SocialMediaLinkSerializer
from django.db import connection
# from django.apps import apps
import json
from django.contrib.auth import get_user_model

User = get_user_model()



# def reset_all_ids_sqlite():
#     for model in apps.get_models():
#         table_name = model._meta.db_table
#         with connection.cursor() as cursor:
#             try:
#                 cursor.execute(f"DELETE FROM {table_name};")  # Deletes all rows
#                 cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table_name}';")  # Resets the AUTOINCREMENT
#                 print(f"Reset IDs for {table_name}")
#             except Exception as e:
#                 print(f"Failed to reset IDs for {table_name}: {e}")

# reset_all_ids_sqlite()



@csrf_exempt
def secret_key_login(request):
    if request.method == 'POST':
        try:
            # Parse JSON body
            body = json.loads(request.body.decode('utf-8'))
            provided_key = body.get('secret_key')

            # Debugging Logs
            print("Received Secret Key:", provided_key)

            # Check if the provided key matches any user's secret_key
            user = User.objects.filter(secret_key=provided_key).first()

            if user:
                request.session['secret_key'] = provided_key
                return JsonResponse({'status': 'success', 'message': 'Access granted'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid key'}, status=400)

        except json.JSONDecodeError as e:
            print("JSON Decode Error:", str(e))
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON payload'}, status=400)

    # Handle unsupported methods
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


def reset_ids(model):
    """
    Resets the IDs of a given model sequentially.
    """
    # Reset the auto-increment sequence for the model
    with connection.cursor() as cursor:
        cursor.execute(f"DELETE FROM sqlite_sequence WHERE name = '{model._meta.db_table}'")

    # Fetch all records in ascending order and update their IDs
    records = model.objects.all().order_by('id')
    for new_id, record in enumerate(records, start=1):
        record.id = new_id
        record.save()

    print(f"IDs reset successfully for {model.__name__}")





@api_view(['GET'])
def search(request):
    query = request.GET.get('query', '').strip()

    if not query:
        return Response({'error': 'No query provided'}, status=400)

    # Dynamic Model Search
    product_results = ProductInfo.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query)
    ).values('id', 'name', 'description')

    devis_results = DevisDemande.objects.filter(
        Q(name__icontains=query) |
        Q(email__icontains=query) |
        Q(address__icontains=query)
    ).values('id', 'name', 'email', 'address')

    contact_results = ContactMessage.objects.filter(
        Q(name__icontains=query) |
        Q(email__icontains=query) |
        Q(message__icontains=query)
    ).values('id', 'name', 'email')

    # Static Page Content
    static_pages = [
        {
            "title": "À propos de nous",
            "content": """
                Nous sommes une entreprise spécialisée dans la création de cheminées de haute qualité,
                combinant tradition et innovation pour offrir à nos clients des solutions uniques et élégantes.
                Rénovations de qualité. Garanti.
            """,
            "url": "/a-propos"
        },
        {
            "title": "Nos Produits",
            "content": """
                Découvrez notre gamme complète de cheminées modernes et classiques,
                ainsi que des accessoires de cheminées de qualité supérieure.
            """,
            "url": "/nos-produits"
        },
        {
            "title": "Demander un Devis",
            "content": """
                Soumettez une demande de devis pour vos projets de rénovation. Remplissez le formulaire
                avec vos coordonnées et vos besoins spécifiques.
            """,
            "url": "/demander-devis"
        },
        {
            "title": "Contact",
            "content": """
                Contactez-nous pour toute question ou assistance. Email: kharrat.deco@gmail.com.
                Téléphone: +216 98 802 080.
            """,
            "url": "/contact"
        },
    ]

    # Fuzzy Matching for Static Pages
    static_results = [
        page for page in static_pages
        if query.lower() in page["content"].lower() or query.lower() in page["title"].lower()
        or difflib.get_close_matches(query.lower(), page["content"].lower().split(), n=1)
    ]

    # Combine Results
    results = {
        "products": list(product_results),
        "devis": list(devis_results),
        "contacts": list(contact_results),
        "static": static_results,
    }

    return Response(results)


###############################################
######## Contact Info links


class ContactInfoViewSet(ModelViewSet):
    queryset = GeneralContactInfo.objects.all()
    serializer_class = GeneralContactInfoSerializer


class SocialMediaViewSet(ModelViewSet):
    queryset = SocialMediaLink.objects.all()
    serializer_class = SocialMediaLinkSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def list_contact_info(request):
    general_info = GeneralContactInfo.objects.all()
    social_links = SocialMediaLink.objects.all()
    return Response({
        "general": GeneralContactInfoSerializer(general_info, many=True).data,
        "social": SocialMediaLinkSerializer(social_links, many=True).data,
    })


@api_view(['PUT'])
@permission_classes([AllowAny])
def update_general_info(request, pk):
    try:
        contact = GeneralContactInfo.objects.get(pk=pk)
    except GeneralContactInfo.DoesNotExist:
        return Response({"error": "General contact info not found"}, status=404)

    serializer = GeneralContactInfoSerializer(contact, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(['PUT'])
@permission_classes([AllowAny])
def update_social_link(request, pk):
    try:
        social_link = SocialMediaLink.objects.get(pk=pk)
    except SocialMediaLink.DoesNotExist:
        return Response({"error": "Social link not found"}, status=404)

    serializer = SocialMediaLinkSerializer(social_link, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


#######################################################
#########################################################







class DevisDemandeViewSet(viewsets.ModelViewSet):
    queryset = DevisDemande.objects.all()
    serializer_class = DevisDemandeSerializer

class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

@method_decorator(ensure_csrf_cookie, name='dispatch')
class ProductInfoViewSet(viewsets.ModelViewSet):
    queryset = ProductInfo.objects.all()
    serializer_class = ProductInfoSerializer
    permission_classes = [AllowAny]
    
    def get_serializer_context(self):
        return {'request': self.request}

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return JsonResponse(serializer.data)


@ensure_csrf_cookie
class ProductCategoryViewSet(ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [IsAuthenticated]


@method_decorator(ensure_csrf_cookie, name='dispatch')
class RealisationViewSet(ModelViewSet):
    queryset = Realisation.objects.all().order_by('-created_at')
    serializer_class = RealisationSerializer
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        return {'request': self.request}

    def update(self, request, *args, **kwargs):
        # Log request data for debugging
        print("Request data:", request.data)
        
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)



@permission_classes([IsAuthenticated])
class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

# API to check authentication and role status
@login_required
def auth_status(request):
    if request.user.is_authenticated:
        return JsonResponse({
            'isAuthenticated': True,
            'isSuperuser': request.user.is_superuser,
            'isStaff': request.user.is_staff
        })
    else:
        return JsonResponse({
            'isAuthenticated': False,
            'isSuperuser': False,
            'isStaff': False
        }, status=401)

# CSRF token view for React
def csrf_token_view(request):
    return JsonResponse({'csrfToken': get_token(request)})

def logout_view(request):
    logout(request)
    return JsonResponse({'message': 'Logged out successfully'})


# Check if user is superuser for user management
def superuser_required(view_func):
    decorated_view_func = user_passes_test(lambda u: u.is_superuser, login_url='login')(view_func)
    return decorated_view_func

# Check if user is staff or superuser for CRUD actions
def staff_required(view_func):
    decorated_view_func = user_passes_test(lambda u: u.is_staff or u.is_superuser, login_url='login')(view_func)
    return decorated_view_func



# API Endpoint to list users
@superuser_required
@api_view(['GET'])
def api_list_users(request):
    users = User.objects.values('id', 'username', 'email', 'secret_key')
    return JsonResponse({'users': list(users)}, status=200)

# API Endpoint to add a new user
@superuser_required
@api_view(['POST'])
def api_add_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    secret_key = request.data.get('secret_key', 'default-secret')  # Handle secret_key

    if not (username and email and password):
        return JsonResponse({'error': 'Missing required fields'}, status=400)

    try:
        user = User.objects.create_user(username=username, email=email, password=password)
        user.secret_key = secret_key  # Assign secret_key
        user.save()
        return JsonResponse({'message': 'User created successfully', 'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'secret_key': user.secret_key,
        }}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# API Endpoint to edit an existing user
@superuser_required
@api_view(['GET', 'POST'])
def api_edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        try:
            user.username = request.data.get('username', user.username)
            user.email = request.data.get('email', user.email)
            password = request.data.get('password')
            if password:
                user.set_password(password)
            # Ensure secret_key is updated
            user.secret_key = request.data.get('secret_key', user.secret_key)
            user.save()
            return JsonResponse({'message': 'User updated successfully', 'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'secret_key': user.secret_key,
            }}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # For GET requests, return user data as JSON
    return JsonResponse({'id': user.id, 'username': user.username, 'email': user.email, 'secret_key': user.secret_key}, status=200)

# API Endpoint to delete an existing user
@superuser_required
@api_view(['DELETE'])
def api_delete_user(user, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    reset_ids(User)  # Reset IDs for User model
    return JsonResponse({'message': 'User deleted successfully'}, status=200)


# ---- Traditional Views for HTML Templates user management ---- #

# HTML view for managing users
@superuser_required
def manage_users(request):
    users = User.objects.all()
    return render(request, 'dashboard/manage_users.html', {'users': users})

# HTML view for adding a user
@superuser_required
def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if username and email and password:
            User.objects.create_user(username=username, email=email, password=password)
            return redirect('manage_users')
    return render(request, 'dashboard/add_user.html')

# HTML view for editing a user
@superuser_required
def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        password = request.POST.get('password')
        if password:
            user.set_password(password)
        user.save()
        return redirect('manage_users')
    return render(request, 'dashboard/edit_user.html', {'user': user})

# HTML view for deleting a user
@superuser_required
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        # reset_ids(User)  # Reset IDs for User model
        return redirect('manage_users')
    return render(request, 'dashboard/delete_user_confirm.html', {'user': user})



# Dashboard View
@login_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')


############################  CRUD views for ProductCategory ############################


# Staff or Superuser CRUD views for ProductCategory
@staff_required
def productcategory_list(request):
    categories = ProductCategory.objects.all()
    return render(request, 'dashboard/productcategory_list.html', {'categories': categories})

@staff_required
def productcategory_create(request):
    form = ProductCategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('productcategory_list')
    return render(request, 'dashboard/productcategory_form.html', {'form': form})

@staff_required
def productcategory_update(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    form = ProductCategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect('productcategory_list')
    return render(request, 'dashboard/productcategory_form.html', {'form': form})

@staff_required
def productcategory_delete(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        category.delete()
        reset_ids(ProductCategory)  # Reset IDs for ProductCategory model
        return redirect('productcategory_list')
    return render(request, 'dashboard/productcategory_confirm_delete.html', {'category': category})



# CRUD for ProductCategory
@login_required
def productcategory_list(request):
    categories = ProductCategory.objects.all()
    return render(request, 'dashboard/productcategory_list.html', {'categories': categories})

@login_required
def productcategory_create(request):
    form = ProductCategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('productcategory_list')
    return render(request, 'dashboard/productcategory_form.html', {'form': form})

@login_required
def productcategory_update(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    form = ProductCategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect('productcategory_list')
    return render(request, 'dashboard/productcategory_form.html', {'form': form})

@login_required
def productcategory_delete(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('productcategory_list')
    return render(request, 'dashboard/productcategory_confirm_delete.html', {'category': category})


 ####################### CRUD views for ProductInfo #########################""


@staff_required
def productinfo_list(request):
    products = ProductInfo.objects.all()
    return render(request, 'dashboard/productinfo_list.html', {'products': products})

@staff_required
def productinfo_create(request):
    categories = ProductCategory.objects.all()
    if request.method == 'POST':
        form = ProductInfoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('productinfo_list')
    else:
        form = ProductInfoForm()
    return render(request, 'dashboard/productinfo_form.html', {'form': form, 'categories': categories})

@staff_required
def productinfo_update(request, pk):
    product = get_object_or_404(ProductInfo, pk=pk)
    categories = ProductCategory.objects.all()
    if request.method == 'POST':
        form = ProductInfoForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('productinfo_list')
    else:
        form = ProductInfoForm(instance=product)
    return render(request, 'dashboard/productinfo_form.html', {'form': form, 'categories': categories})

@staff_required
def productinfo_delete(request, pk):
    product = get_object_or_404(ProductInfo, pk=pk)
    if request.method == 'POST':
        product.delete()
        reset_ids(ProductInfo)
        return redirect('productinfo_list')
    return render(request, 'dashboard/productinfo_confirm_delete.html', {'product': product})





@login_required
def productinfo_create(request):
    categories = ProductCategory.objects.all()
    if request.method == 'POST':
        form = ProductInfoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('productinfo_list')
    else:
        form = ProductInfoForm()
    return render(request, 'dashboard/productinfo_form.html', {'form': form, 'categories': categories})

# Update an existing ProductInfo entry
@login_required
def productinfo_update(request, pk):
    product = get_object_or_404(ProductInfo, pk=pk)
    categories = ProductCategory.objects.all()
    if request.method == 'POST':
        form = ProductInfoForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('productinfo_list')
    else:
        form = ProductInfoForm(instance=product)
    return render(request, 'dashboard/productinfo_form.html', {'form': form, 'categories': categories})

# Delete a ProductInfo entry
@login_required
def productinfo_delete(request, pk):
    product = get_object_or_404(ProductInfo, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('productinfo_list')
    return render(request, 'dashboard/productinfo_confirm_delete.html', {'product': product})






########## CRUD for Realisation ###########

# CRUD for Realisation
@staff_required
def realisation_list(request):
    realisations = Realisation.objects.all()
    return render(request, 'dashboard/realisation_list.html', {'realisations': realisations})

# Create a new Realisation
@staff_required
def realisation_create(request):
    categories = ProductCategory.objects.all()  # Fetch all categories
    print("Categories passed to template:", categories)  # Debug line to verify categories

    if request.method == 'POST':
        form = RealisationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('realisation_list')
    else:
        form = RealisationForm()
    return render(request, 'dashboard/realisation_form.html', {'form': form, 'categories': categories})


# Update an existing Realisation
@staff_required
def realisation_update(request, pk):
    realisation = get_object_or_404(Realisation, pk=pk)
    categories = ProductCategory.objects.all()
    if request.method == 'POST':
        form = RealisationForm(request.POST, request.FILES, instance=realisation)
        if form.is_valid():
            form.save()
            return redirect('realisation_list')
    else:
        form = RealisationForm(instance=realisation)
    return render(request, 'dashboard/realisation_form.html', {'form': form, 'categories': categories})

# Delete a Realisation
@staff_required
def realisation_delete(request, pk):
    realisation = get_object_or_404(Realisation, pk=pk)
    if request.method == 'POST':
        realisation.delete()
        reset_ids(Realisation)  # Reset IDs for Realisation model
        return redirect('realisation_list')
    return render(request, 'dashboard/realisation_confirm_delete.html', {'realisation': realisation})




@login_required
def realisation_list(request):
    realisations = Realisation.objects.all()
    return render(request, 'dashboard/realisation_list.html', {'realisations': realisations})

# Create a new Realisation
@login_required
def realisation_create(request):
    categories = ProductCategory.objects.all()  # Fetch all categories
    print("Categories passed to template:", categories)  # Debug line to verify categories

    if request.method == 'POST':
        form = RealisationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('realisation_list')
    else:
        form = RealisationForm()
    return render(request, 'dashboard/realisation_form.html', {'form': form, 'categories': categories})


# Update an existing Realisation
@login_required
def realisation_update(request, pk):
    realisation = get_object_or_404(Realisation, pk=pk)
    categories = ProductCategory.objects.all()
    if request.method == 'POST':
        form = RealisationForm(request.POST, request.FILES, instance=realisation)
        if form.is_valid():
            form.save()
            return redirect('realisation_list')
    else:
        form = RealisationForm(instance=realisation)
    return render(request, 'dashboard/realisation_form.html', {'form': form, 'categories': categories})

# Delete a Realisation
@login_required
def realisation_delete(request, pk):
    realisation = get_object_or_404(Realisation, pk=pk)
    if request.method == 'POST':
        realisation.delete()
        return redirect('realisation_list')
    return render(request, 'dashboard/realisation_confirm_delete.html', {'realisation': realisation})









###################### CRUD for DevisDemande ##########################""""
@staff_required
def devisdemande_list(request):
    demandes = DevisDemande.objects.all()
    return render(request, 'dashboard/devisdemande_list.html', {'demandes': demandes})

@staff_required
def devisdemande_detail(request, pk):
    demande = get_object_or_404(DevisDemande, pk=pk)
    return render(request, 'dashboard/devisdemande_detail.html', {'demande': demande})

@staff_required
def test_devisdemande_update_status(request, pk):
    if request.method == 'POST':
        # Retrieve the DevisDemande instance
        demande = get_object_or_404(DevisDemande, pk=pk)
        
        # Retrieve values from POST data and update instance fields
        customer_contacted = request.POST.get('customer_contacted') == 'true'
        request_completed = request.POST.get('request_completed') == 'true'
        
        # Apply the updates to the model instance
        demande.customer_contacted = customer_contacted
        demande.request_completed = request_completed
        
        # Save changes to the database
        demande.save()

        # Send a success response back to the frontend
        return JsonResponse({
            'status': 'success',
            'customer_contacted': demande.customer_contacted,
            'request_completed': demande.request_completed,
            'message': 'Devis demande status updated successfully'
        })
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)


@staff_required
def devisdemande_delete(request, pk):
    demande = get_object_or_404(DevisDemande, pk=pk)
    if request.method == 'POST':
        demande.delete()
        reset_ids(DevisDemande)  # Reset IDs for DevisDemande model
        return redirect('devisdemande_list')
    return render(request, 'dashboard/devisdemande_confirm_delete.html', {'demande': demande})




@login_required
def devisdemande_list(request):
    demandes = DevisDemande.objects.all()
    return render(request, 'dashboard/devisdemande_list.html', {'demandes': demandes})

@login_required
def devisdemande_detail(request, pk):
    demande = get_object_or_404(DevisDemande, pk=pk)
    return render(request, 'dashboard/devisdemande_detail.html', {'demande': demande})


@login_required
def devisdemande_update_status(request, pk):
    demande = get_object_or_404(DevisDemande, pk=pk)
    if request.method == 'POST':
        demande.customer_contacted = 'customer_contacted' in request.POST
        demande.request_completed = 'request_completed' in request.POST
        demande.save()
        return redirect('devisdemande_list')
    return render(request, 'dashboard/devisdemande_status_form.html', {'demande': demande})

@login_required
def devisdemande_delete(request, pk):
    demande = get_object_or_404(DevisDemande, pk=pk)
    if request.method == 'POST':
        demande.delete()
        return redirect('devisdemande_list')
    return render(request, 'dashboard/devisdemande_confirm_delete.html', {'demande': demande})






#############"" CRUD for ContactMessage ########################
@staff_required
def contactmessage_list(request):
    contactmessages = ContactMessage.objects.all()
    return render(request, 'dashboard/contactmessage_list.html', {'contactmessages': contactmessages})

@staff_required
def contactmessage_detail(request, pk):
    contactmessage = get_object_or_404(ContactMessage, pk=pk)
    return render(request, 'dashboard/contactmessage_detail.html', {'contactmessage': contactmessage})

@csrf_exempt
@staff_required
def test_contactmessage_update_status(request, pk):
    if request.method == 'POST':
        message = get_object_or_404(ContactMessage, pk=pk)
        message.customer_contacted = request.POST.get('customer_contacted') == 'true'
        message.request_completed = request.POST.get('request_completed') == 'true'
        message.save()

        return JsonResponse({
            'status': 'success',
            'customer_contacted': message.customer_contacted,
            'request_completed': message.request_completed,
            'message': 'Contact message status updated successfully'
        })
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@staff_required
def contactmessage_delete(request, pk):
    contactmessage = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST':
        contactmessage.delete()
        reset_ids(ContactMessage)  # Reset IDs for ContactMessage model

        return redirect('contactmessage_list')
    return render(request, 'dashboard/contactmessage_confirm_delete.html', {'contactmessage': contactmessage})









@login_required
def contactmessage_list(request):
    contactmessages = ContactMessage.objects.all()
    return render(request, 'dashboard/contactmessage_list.html', {'contactmessages': contactmessages})

@login_required
def contactmessage_detail(request, pk):
    contactmessage = get_object_or_404(ContactMessage, pk=pk)
    return render(request, 'dashboard/contactmessage_detail.html', {'contactmessage': contactmessage})

@login_required
def contactmessage_update_status(request, pk):
    if request.method == 'POST':
        contactmessage = get_object_or_404(ContactMessage, pk=pk)
        contactmessage.customer_contacted = 'customer_contacted' in request.POST
        contactmessage.request_completed = 'request_completed' in request.POST
        contactmessage.save()
        return redirect('contactmessage_detail', pk=pk)
    
@login_required
def contactmessage_delete(request, pk):
    contactmessage = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST':
        contactmessage.delete()
        return redirect('contactmessage_list')
    return render(request, 'dashboard/contactmessage_confirm_delete.html', {'contactmessage': contactmessage})


