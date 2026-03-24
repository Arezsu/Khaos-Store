from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django import forms
from .models import Product, Order, UserProfile

# ==================== FORMULARIO PERSONALIZADO PARA PRODUCTO ====================
class ProductForm(forms.ModelForm):
    image = forms.URLField(
        label='URL de imagen',
        required=True,
        help_text='Pega aquí la URL de la imagen (ej: https://res.cloudinary.com/... o cualquier URL de imagen)'
    )
    
    class Meta:
        model = Product
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.image:
            self.fields['image'].initial = self.instance.image.url if hasattr(self.instance.image, 'url') else self.instance.image

# ==================== PRODUCTOS ====================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display = ['id', 'name', 'price', 'stock', 'is_on_sale', 'image_display', 'created_at']
    list_display_links = ['id', 'name']
    list_filter = ['is_on_sale', 'category', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['stock', 'is_on_sale']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {
            'fields': ('name', 'price', 'image', 'description', 'stock', 'is_on_sale', 'sale_price', 'category')
        }),
        ('Fechas', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def image_display(self, obj):
        if obj.image:
            return f'<a href="{obj.image}" target="_blank">Ver imagen</a>'
        return 'Sin imagen'
    image_display.allow_tags = True
    image_display.short_description = 'Imagen'

# ==================== ÓRDENES ====================
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer_name', 'product', 'total', 'status', 'created_at']
    list_display_links = ['order_number', 'customer_name']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['order_number', 'customer_name', 'customer_email']
    list_editable = ['status']
    readonly_fields = ['order_number', 'created_at']
    ordering = ['-created_at']

# ==================== PERFILES ====================
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'city']
    search_fields = ['user__username', 'user__email', 'phone']

# ==================== USUARIOS ====================
admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']
    search_fields = ['username', 'email']
    list_editable = ['is_active']
    actions = ['delete_selected']

# ==================== PERSONALIZACIÓN ====================
admin.site.site_header = 'Khaos Store Admin'
admin.site.site_title = 'Khaos Store'
admin.site.index_title = 'Panel de Administración'