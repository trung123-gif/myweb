import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myweb.settings')
django.setup()

from myapp.models import Category, Discount, Product, ThanhPho, QuanHuyen, PhuongXa, User, Feedback, Status, Order, Image
from myapp.models import Card, CPU, RAM, Harddrive ,ManHinh, Loai, Laptop, Brand, Age, Chitietdonhang
