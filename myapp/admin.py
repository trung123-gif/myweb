from django.contrib import admin

# Register your models here.
from .models import Category, Discount, Product, ThanhPho, QuanHuyen, PhuongXa, User, Feedback, Status, Order, Image
from. models import Card, CPU, RAM, Harddrive ,ManHinh, Loai, Laptop, Brand, Age, Detail, Chitietdonhang
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_parent', 'image']

class DiscountAdmin(admin.ModelAdmin):
    list_display = ['discount', 'date_start', 'date_end']

class LoaiAdmin(admin.ModelAdmin):
    list_display = ['loai']

class BrandAdmin(admin.ModelAdmin):
    list_display = ['brand', 'image']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'category', 'loai', 'age', 'brand', 'discount', 'detail', 'soluong', 'price']

class CardAdmin(admin.ModelAdmin):
    list_display = ['product', 'chip', 'memory', 'connector','psu', 'socketsupport', 'image']

class CPUAdmin(admin.ModelAdmin):
    list_display = ['product', 'socket', 'core', 'speed', 'cache', 'TDP', 'card', 'image']

class RAMAdmin(admin.ModelAdmin):
    list_display = ['product', 'standram', 'capacity', 'speed', 'image']

class HarddriveAdmin(admin.ModelAdmin):
    list_display = ['product', 'loai', 'standard', 'size', 'memory', 'image']

class ManHinhAdmin(admin.ModelAdmin):
    list_display = ['product', 'size', 'resolution', 'panels', 'frequency', 'connector', 'image']

class LaptopAdmin(admin.ModelAdmin):
    list_display = ['product', 'cpu', 'ram', 'harddrive', 'card', 'manhinh', 'image']

class ThanhPhoAdmin(admin.ModelAdmin):
    list_display = ['id','thanhpho', 'loai']

class QuanHuyenAdmin(admin.ModelAdmin):
    list_display = ['quanhuyen', 'thanhpho', 'loai']

class PhuongXaAdmin(admin.ModelAdmin):
    list_display = ['phuongxa', 'quanhuyen', 'loai']

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'password', 'fullname', 'first_name', 'last_name', 'ngaysinh', 'email', 'phone', 'diachi', 'phuongxa', 'quanhuyen', 'thanhpho', 'save_password']

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['content', 'user', 'product', 'vote', 'date']

class StatusAdmin(admin.ModelAdmin):
    list_display = ['status']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['date', 'user', 'status']

class ImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image']

class AgeAdmin(admin.ModelAdmin):
    list_display = ['age']

class SaleAdmin(admin.ModelAdmin):
    list_display = ['sale']

class DetailAdmin(admin.ModelAdmin):
    list_display = ['detail']

class ChitietdonhangAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'soluong', 'money']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ThanhPho, ThanhPhoAdmin)
admin.site.register(QuanHuyen, QuanHuyenAdmin)
admin.site.register(PhuongXa, PhuongXaAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Laptop, LaptopAdmin)
admin.site.register(Image, ImageAdmin)

admin.site.register(Card, CardAdmin)
admin.site.register(CPU, CPUAdmin)
admin.site.register(RAM, RAMAdmin)
admin.site.register(Harddrive, HarddriveAdmin)
admin.site.register(ManHinh, ManHinhAdmin)
admin.site.register(Loai, LoaiAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Age, AgeAdmin)
admin.site.register(Detail, DetailAdmin)
admin.site.register(Chitietdonhang, ChitietdonhangAdmin)


