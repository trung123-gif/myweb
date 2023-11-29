import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myweb.settings')
django.setup()

from myapp.models import Category, Discount, Product, ThanhPho, QuanHuyen, PhuongXa, User, Feedback, Status, Order, Image
from myapp.models import Card, CPU, RAM, Harddrive ,ManHinh, Loai, Laptop, Brand, Age, Chitietdonhang


a = User.objects.get(username="thanhtrung0599")
a.set_password('trung4049')
a.save()

from django.contrib.auth.hashers import check_password, make_password

print(check_password('trung4049', a.password))