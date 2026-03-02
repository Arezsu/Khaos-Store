from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Order, UserProfile
from datetime import date
import traceback

def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        phone = request.POST.get('phone', '')
        birth_year = request.POST.get('birth_year')
        birth_month = request.POST.get('birth_month')
        birth_day = request.POST.get('birth_day')
        
        # Validaciones
        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden')
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El usuario ya existe')
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'El email ya está registrado')
            return redirect('register')
        
        if len(phone) != 10 or not phone.isdigit():
            messages.error(request, 'El teléfono debe tener exactamente 10 dígitos')
            return redirect('register')
        
        # Validar edad
        try:
            birth_date = date(int(birth_year), int(birth_month), int(birth_day))
            today = date.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            if age < 18:
                messages.error(request, 'Debes ser mayor de 18 años para registrarte')
                return redirect('register')
        except:
            messages.error(request, 'Fecha de nacimiento inválida')
            return redirect('register')
        
        # Crear usuario
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        # Crear perfil
        UserProfile.objects.create(
            user=user,
            phone=phone,
            birth_date=birth_date
        )
        
        login(request, user)
        messages.success(request, '¡Registro exitoso! Bienvenido a KHAOS STORE')
        
        next_url = request.POST.get('next') or request.GET.get('next')
        if next_url:
            return redirect(next_url)
        return redirect('home')
    
    return render(request, 'store/register.html')

@login_required(login_url='login')
def checkout(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/checkout.html', {'product': product})

@login_required(login_url='login')
def process_payment(request, product_id):
    # SOLO ACEPTAR POST
    if request.method != 'POST':
        return redirect('home')
    
    try:
        print("=" * 50)
        print("🔍 INICIANDO PROCESO DE PAGO")
        
        # Obtener producto
        product = get_object_or_404(Product, id=product_id)
        
        # Verificar stock
        if product.stock <= 0:
            messages.error(request, 'Producto agotado')
            return redirect('home')
        
        # VALIDAR CAMPOS OBLIGATORIOS
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        payment_method = request.POST.get('payment_method', 'CARD')
        
        if not name:
            messages.error(request, 'El nombre es obligatorio')
            return redirect('checkout', product_id=product.id)
        
        if not email:
            messages.error(request, 'El email es obligatorio')
            return redirect('checkout', product_id=product.id)
        
        if not phone or len(phone) != 10 or not phone.isdigit():
            messages.error(request, 'El teléfono debe tener exactamente 10 dígitos')
            return redirect('checkout', product_id=product.id)
        
        # Crear la orden
        order = Order.objects.create(
            product=product,
            customer_name=name,
            customer_email=email,
            customer_phone=phone,
            address='No requerida',
            city='No requerida',
            payment_method=payment_method,
            total=product.get_price(),
            user=request.user,
            status='PAID'
        )
        
        # Restar stock
        product.stock -= 1
        product.save()
        
        # ENVIAR EMAILS
        print("📧 Enviando emails...")
        order.send_confirmation_email()
        order.send_game_key()
        
        # Guardar en sesión
        request.session['last_order'] = order.order_number
        
        messages.success(request, '¡Pago exitoso! Revisa tu correo')
        return redirect('success', order_id=order.order_number)
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        messages.error(request, 'Error al procesar el pago')
        return redirect('home')

def success(request, order_id):
    return render(request, 'store/success.html', {'order_id': order_id})

@login_required(login_url='login')
def profile(request):
    user_profile = UserProfile.objects.get_or_create(user=request.user)[0]
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/profile.html', {
        'profile': user_profile,
        'orders': orders
    })