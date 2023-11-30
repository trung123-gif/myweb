from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import datetime, timedelta
class Category(models.Model):
    name = models.CharField(max_length=255)
    category_parent = models.ForeignKey(
        to='self',
        blank=True,
        null=True,
        on_delete= models.CASCADE
        )
    image = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        return f'{self.name}'
    class Meta:
        db_table = 'Category'
        ordering = ['pk']

class Discount(models.Model):
    discount = models.IntegerField()
    date_start = models.DateTimeField(null=True, blank=True, default=datetime.now())
    date_end = models.DateTimeField(null=True, blank=True, default=datetime.now()+ timedelta(days=2))
    def __str__(self):
        return f'{self.discount}%'
    class Meta:
        db_table = 'Discount'

class Loai(models.Model):
    loai = models.CharField(max_length=255)
    def __str__(self):
        return f'{self.loai}'
    class Meta:
        db_table = 'Loai'

class Age(models.Model):
    age = models.CharField(max_length=255)
    def __str__(self):
        return f'{self.age}'
    class Meta:
        db_table = 'Age'

class Brand(models.Model):
    brand = models.CharField(max_length=30)
    image = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        return f'{self.brand}'
    class Meta:
        db_table = 'Brand'

class Detail(models.Model):
    detail = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        return f'{self.detail}'
    class Meta:
        db_table = 'detail'

class Product(models.Model):
    name = models.CharField(max_length=255, unique= True)
    description = models.TextField(null=True, blank=True)
    loai = models.ForeignKey(to = Loai, on_delete= models.CASCADE, null=True, blank=True)
    age = models.ForeignKey(to = Age, on_delete= models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(to = Category, on_delete= models.CASCADE)
    brand = models.ForeignKey(to = Brand, on_delete= models.CASCADE, null=True, blank=True)
    discount = models.ForeignKey(to = Discount, on_delete= models.CASCADE, null=True, blank=True)
    detail = models.ForeignKey(to = Detail, on_delete= models.CASCADE, null=True, blank=True)
    soluong = models.IntegerField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return f'{self.name}'
    class Meta:
        db_table = 'Product'

class Image(models.Model):
    product = models.ForeignKey(to = Product, on_delete= models.CASCADE)
    image = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        return f'{self.product}'
    class Meta:
        db_table = 'Image'

class Card(models.Model):
    product = models.OneToOneField(to = Product, on_delete= models.CASCADE)
    chip = models.CharField(max_length=30, null=True, blank=True)
    memory = models.CharField(max_length=30, null=True, blank=True)
    connector = models.CharField(max_length=30, null=True, blank=True)
    socketsupport = models.CharField(max_length=30, null=True, blank=True)
    psu = models.CharField(max_length=30, null=True, blank=True)
    image = models.OneToOneField(to = Image, on_delete= models.CASCADE, null=True, blank=True)
    def __str__(self):
        return f'{self.product}'
    class Meta:
        db_table = 'Card'
    def values(self):
        return {
            'Chip đồ họa:':self.chip, 
            'Bộ nhớ:':self.memory, 
            'PSU tối thiểu:':self.connector, 
            'Cổng kết nối:': self.psu,
            }

class CPU(models.Model):
    product = models.OneToOneField(to = Product, on_delete= models.CASCADE)
    socket = models.CharField(max_length=30, null=True, blank=True)
    core = models.CharField(max_length=30, null=True, blank=True)
    speed = models.CharField(max_length=30, null=True, blank=True)
    cache = models.CharField(max_length=30, null=True, blank=True)
    TDP = models.CharField(max_length=30, null=True, blank=True)
    card = models.ForeignKey(to = Card, on_delete= models.CASCADE, null=True, blank=True)
    image = models.OneToOneField(to = Image, on_delete= models.CASCADE, null=True, blank=True)
    def __str__(self):
        return f'{self.product}'
    class Meta:
        db_table = 'CPU'
    def values(self):
        return {
            'Socket:':self.socket, 
            'Nhân - Luồng:':self.core, 
            'Tốc độ:':self.speed, 
            'Bộ nhớ đệm': self.cache,
            'TDP': self.TDP,
            }

class RAM(models.Model):
    product = models.OneToOneField(to = Product, on_delete= models.CASCADE)
    standram = models.CharField(max_length=30, null=True, blank=True)
    capacity = models.CharField(max_length=30, null=True, blank=True)
    speed = models.CharField(max_length=30, null=True, blank=True)
    image = models.OneToOneField(to = Image, on_delete= models.CASCADE, null=True, blank=True)
    def __str__(self):
        return f'{self.product}'
    class Meta:
        db_table = 'RAM'
    def values(self):
        return {
            'Chuẩn:':self.standram, 
            'Dung lượng:':self.capacity, 
            'Bus RAM:':self.speed, 
            }

class Harddrive(models.Model):
    product = models.OneToOneField(to = Product, on_delete= models.CASCADE)
    loai = models.CharField(max_length=30, null=True, blank=True)
    standard = models.CharField(max_length=30, null=True, blank=True)
    size = models.CharField(max_length=30, null=True, blank=True)
    memory = models.CharField(max_length=30, null=True, blank=True)
    image = models.OneToOneField(to = Image, on_delete= models.CASCADE, null=True, blank=True)
    def __str__(self):
        return f'{self.product}'
    class Meta:
        db_table = 'Harddrive'
    def values(self):
        return {
            'Loại ổ:':self.loai, 
            'Chuẩn:':self.standard, 
            'Kích thước:':self.size, 
            'Dung lượng:':self.memory, 
            }

class ManHinh(models.Model):
    product = models.OneToOneField(to = Product, on_delete= models.CASCADE)
    size = models.CharField(max_length=30, null=True, blank=True)
    resolution = models.CharField(max_length=30, null=True, blank=True)
    panels = models.CharField(max_length=30, null=True, blank=True)
    frequency = models.CharField(max_length=30, null=True, blank=True)
    connector = models.CharField(max_length=30, null=True, blank=True)
    image = models.OneToOneField(to = Image, on_delete= models.CASCADE, null=True, blank=True)
    def __str__(self):
        return f'{self.product}'
    class Meta:
        db_table = 'ManHinh'
    def values(self):
        return {
            'Kích thước:':self.size, 
            'Độ phân giải:':self.resolution, 
            'Tấm nền:':self.panels, 
            'Tần số quét:':self.frequency, 
            'Cổng kết nối:':self.connector}

class Laptop(models.Model):
    product = models.OneToOneField(to = Product, on_delete= models.CASCADE)
    cpu = models.ForeignKey(to = CPU, on_delete= models.CASCADE, null=True, blank=True)
    ram = models.ForeignKey(to = RAM, on_delete= models.CASCADE, null=True, blank=True)
    harddrive = models.ForeignKey(to = Harddrive, on_delete= models.CASCADE, null=True, blank=True)
    card = models.ForeignKey(to = Card, on_delete= models.CASCADE, null=True, blank=True)
    manhinh = models.ForeignKey(to = ManHinh, on_delete= models.CASCADE, null=True, blank=True)
    image = models.OneToOneField(to = Image, on_delete= models.CASCADE, null=True, blank=True)
    def __str__(self):
        return f'{self.product}'
    
    class Meta:
        db_table = 'Laptop'

    def values(self):
        return {
            'CPU:':self.cpu.product.name, 
            'RAM:':self.ram.product.name, 
            'Ổ Cứng:':self.harddrive.product.name, 
            'Card:':self.card.product.name, 
            'Màn Hình:':self.manhinh.product.name}

class ThanhPho(models.Model):
    id = models.IntegerField(primary_key=True)
    thanhpho= models.CharField(max_length=100)
    loai = models.CharField(max_length=30, null=True, blank=True)
    def __str__(self):
        return f'{self.thanhpho}'
    class Meta:
        db_table = 'ThanhPho'
        ordering = ['pk']

class QuanHuyen(models.Model):
    id = models.IntegerField(primary_key=True)
    quanhuyen = models.CharField(max_length=100)
    loai = models.CharField(max_length=30, null=True, blank=True)
    thanhpho = models.ForeignKey(to = ThanhPho, on_delete= models.CASCADE)
    def __str__(self):
        return f'{self.quanhuyen}'
    class Meta:
        db_table = 'QuanHuyen'
        ordering = ['pk']

class PhuongXa(models.Model):
    id = models.IntegerField(primary_key=True)
    phuongxa = models.CharField(max_length=100)
    loai = models.CharField(max_length=30, null=True, blank=True)
    quanhuyen = models.ForeignKey(to = QuanHuyen, on_delete= models.CASCADE)
    def __str__(self):
        return f'{self.phuongxa}'
    class Meta:
        db_table = 'PhuongXa'
        ordering = ['pk']

class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    fullname = models.CharField(max_length=100)
    ngaysinh = models.DateField(null=True)
    phone = models.CharField(max_length=20)
    diachi = models.TextField()
    thanhpho = models.ForeignKey(to = ThanhPho, on_delete= models.CASCADE, null=True)
    quanhuyen = models.ForeignKey(to = QuanHuyen, on_delete= models.CASCADE, null=True)
    phuongxa = models.ForeignKey(to = PhuongXa, on_delete= models.CASCADE, null=True)
    save_password = models.CharField(max_length=255, null=True)
    def __str__(self):
        return f'{self.username}'
    class Meta:
        db_table = 'User'

class Feedback(models.Model):
    content = models.TextField()
    user = models.ForeignKey(to = User, on_delete= models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(to = Product, on_delete= models.DO_NOTHING, null=True, blank=True)
    vote = models.IntegerField(null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'Feedback'

class Status(models.Model):
    status = models.CharField(max_length=40)
    def __str__(self):
        return f'{self.id, self.status}'
    class Meta:
        db_table = 'Status'

class Order(models.Model):
    date = models.DateTimeField(null=True, blank=True)
    status = models.ForeignKey(to = Status, on_delete= models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(to = User, on_delete= models.CASCADE)
    def __str__(self):
        return f'Đơn {self.user} {self.date} {self.id}'
    class Meta:
        db_table = 'Order'

class Chitietdonhang(models.Model):
    order = models.ForeignKey(to = Order, on_delete= models.CASCADE)
    product = models.ForeignKey(to = Product, on_delete= models.CASCADE)
    soluong = models.IntegerField(null=True, blank=True)
    money = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return f'Thông tin đơn hàng {self.order}'
    class Meta:
        db_table = 'Chitietdonhang'

