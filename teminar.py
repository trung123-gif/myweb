import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myweb.settings')
django.setup()

from myapp.models import Category, Discount, Product, ThanhPho, QuanHuyen, PhuongXa, User, Feedback, Status, Order, Image
from myapp.models import Card, CPU, RAM, Harddrive ,ManHinh, Loai, Laptop, Brand, Age, Chitietdonhang

type = Loai.objects.filter(loai__icontains = 'Laptop')
for i in type:
    print(i.id)
    
print(type)
# laptops_new = Product.objects.filter(loai_id__in = [3,4,5,6,7])
# print(laptops_new)