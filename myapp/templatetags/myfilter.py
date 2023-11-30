from django import template
register = template.Library()
from myapp.models import Category, Discount, Product, ThanhPho, QuanHuyen, PhuongXa, User, Feedback, Status, Order, Image
from myapp.models import Card, CPU, RAM, Harddrive ,ManHinh, Loai, Laptop, Brand, Age, Chitietdonhang
from django.db.models import Q
from datetime import datetime

@register.filter()
def count_item_brand(name_brand):
    brand = Brand.objects.get(brand=name_brand)
    return len(list(Product.objects.filter(~Q(age_id=3), brand_id = brand.id)))

@register.filter()
def get_image_laptop(id):
    return Laptop.objects.get(product_id = id).image.image

@register.filter()
def get_image(id):
    models = [Card, CPU, Laptop, RAM, ManHinh, Harddrive]
    for model in models:
        try:
            product = model.objects.get(product_id = id)
            return product.image.image
        except model.DoesNotExist:
            continue

@register.filter()
def price_sale(price, sale):
    return int(price*(100-sale)/100)

@register.filter()
def len_filter(iterable):
    return len(iterable)

@register.filter()
def make_range(num):
    return range(1,num+1)

@register.filter()
def make_url(url):
    list_url = url.split('&',1)
    return list_url[0]

@register.filter()
def product_values(id):
    models = [Card, CPU, Laptop, RAM, ManHinh, Harddrive]
    for model in models:
        try:
            product = model.objects.get(product_id = id)
            return product.values()
        except model.DoesNotExist:
            continue

@register.filter()
def make_dict(dic, key):
    return dic[key]

@register.filter()
def icon_user(str):
    return str[0].upper()

@register.filter()
def count_product_cart(user):
    try:
        order = Order.objects.get(user=user, status_id = 1)
        dh = order.chitietdonhang_set.all()
        counts = 0
        for count in dh:
            counts+=count.soluong
        return counts
    except Order.DoesNotExist:
        return 0

@register.filter()
def price_one_producr(price, count):
    return int(price/count)

@register.filter()
def count_product(chitiethoadon):
    return chitiethoadon.product.soluong

@register.filter()
def get_image_product(product_id):
    model_list = [Card, CPU, RAM, Harddrive, ManHinh, Laptop]
    for model in model_list:
        try:
            product = model.objects.get(product_id=product_id)
            return product.image.image
        except model.DoesNotExist:
            continue

@register.filter()
def fomat_money(price):
    money = ''
    k = 0
    for i in range(len(str(price))):
        du = price%10
        price = price//10

        if k == 3:
            money = str(du)+'.'+ money
            k=0
        else:
            money = str(du) + money
        k+=1
    return money + ' VNĐ'

@register.filter()
def date_order(order):
    return order.strftime("%Y/%m/%d %H:%M:%S")

@register.filter()
def make_range(number):
    return range(0, number)

@register.filter()
def so_sanh(number1, number2):
    return number1 > number2

