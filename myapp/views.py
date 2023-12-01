from django.shortcuts import render, redirect
from .models import Category, Discount, Product, ThanhPho, QuanHuyen, PhuongXa, User, Feedback, Status, Order, Image
from .models import Card, CPU, RAM, Harddrive ,ManHinh, Loai, Laptop, Brand, Age, Chitietdonhang
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import RegisterForm, UserLoginForm, OrderForm, OrderCreateForm, ChangePassword, ContactForm, ForgotPasswordForm, TokenPasswordForm
from django.http.response import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.utils import timezone
from django.core.mail import BadHeaderError
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template import loader
from django.contrib.auth.hashers import check_password
from django.contrib.auth.tokens import default_token_generator 
# Create your views here.

## Trang Chủ Start
def index(request):
    categories = Category.objects.all()
    types = Loai.objects.all()
    data_type = []
    for i in Loai.objects.filter(loai__icontains = 'Laptop'):
        data_type.append(i.id)
    brands = Brand.objects.filter(brand__in=['Dell', 'Asus', 'HP', 'Lenovo', 'Intel', 'AMD'])
    laptops_sale = Product.objects.filter(loai_id__in = data_type, age_id = 1).order_by('-discount')[:12]
    # Lấy 12 laptop có discount giảm dần
    laptops_new = Product.objects.filter(loai_id__in = data_type, age_id = 1).order_by('-id')[:12]
    # Lấy 12 laptop mới được thêm vào
    return render(
        request=request,
        template_name= 'index.html',
        context= {
            'categories': categories,
            'types': types,
            'brands': brands,
            'sales': laptops_sale,
            'news': laptops_new,
        }
    )
## Trang Chủ End

## Trang Views Start
def views(request):
    categories = Category.objects.all()
    type = Loai.objects.all()
    brands = Brand.objects.all()
    if request.method == "GET":
        # Lấy giá trị từ khóa 
        key_word_category = request.GET.get('category')
        type_category = request.GET.get('type')
        brand_product = request.GET.get('brand')
        sale_all = request.GET.get('sale')
        new_all = request.GET.get('new')
        price_all = request.GET.get('price')
        search = request.GET.get('search')
        latest = request.GET.get('latest')
        old = request.GET.get('old')

        # Dach sách chứa id danh mục của từ khóa 'category'
        list_data= []
        if key_word_category:
            category_name = Category.objects.get(name = key_word_category)
            # Khi click vào danh mục con
            if category_name.category_parent:
                list_data.append(category_name.id)
            else:
            # Click vào danh mục cha
                if category_name.category_set.all():
                    for category in Category.objects.filter(category_parent_id = category_name.id):
                    # Lấy toàn bộ id danh mục con có parrent_id = id của danh mục cha
                        if category.product_set.all():
                            list_data.append(category.id)
                else:
                    return render(
                            request=request,
                            template_name= '404.html',
                    )
            print(list_data)
            # Lấy ra các sản phẩm có category id có trong danh sách list_data
            products = Product.objects.filter(category__in = list_data, price__isnull=False)

        elif type_category:
            type_id = Loai.objects.get(loai=type_category).id
            list_data.append(type_id)
            products = Product.objects.filter(loai_id__in = list_data, price__isnull=False)
        
        elif brand_product:
            brand_id = Brand.objects.get(brand=brand_product).id
            list_data.append(brand_id)
            products = Product.objects.filter(brand_id__in = list_data, price__isnull=False)
        
        elif sale_all:
            products = Product.objects.filter(discount_id__isnull = False, price__isnull=False)

        elif new_all:
            products = Product.objects.filter(price__isnull=False).order_by('-id')
        
        elif search:
            products = Product.objects.filter(name__icontains = search, price__isnull=False)

        else:
            products = Product.objects.filter(price__isnull=False)
        
        if products:
            message = ''
            # Xử lý tăng giảm theo giá
            if price_all == 'increase':
                products = products.order_by('price')
            elif price_all == 'decrease':
                products = products.order_by('-price')

            # Xử lý sản phẩm mới nhất
            if latest:
                products = products.order_by('-id')
            elif old:
                products = products.order_by('id')
            # Xử lý phân trang
            paginator = Paginator(products, 18)
            page = request.GET.get("page")
            products = paginator.get_page(page)
            message = ''
        else: 
            message = 'Chưa Có Sản Phẩm'

        return render(
            request=request,
            template_name= 'views.html',
            context= {
                'categories': categories,
                'types': type,
                'products': products,
                'message': message,
                'brands': brands,
            }
        )
## Trang Views End

## Trang Detail Start    
def detail(request, id):
    categories = Category.objects.all()
    type = Loai.objects.all()

    # Lấy sản phẩm xem chi tiết
    product = Product.objects.get(id=id)

    # Lấy ra các sản phẩm cùng loại, cùng brand start
    brand = product.brand.id
    type_new = product.loai.id
    products_similar = Product.objects.filter(brand_id = brand, loai_id = type_new, price__isnull=False)
    # Lấy ra các sản phẩm cùng loại, cùng brand end

    # Review
    reviews = Feedback.objects.filter(product = product)
    tb_vote = 0
    if reviews:
        sum_vote = 0
        for vote in reviews:
            sum_vote+=vote.vote
        tb_vote = sum_vote//len(reviews)
    return render(
        request=request,
        template_name= 'detail.html',
        context= {
            'product': product,
            'categories': categories,
            'types': type,
            'images': product.image_set.all(),
            'products_similar': products_similar,
            'reviews': reviews,
            'tb_vote': tb_vote
        }
    )
## Trang Detail End

## Add product bằng button add start
@login_required(login_url='login_user_url')
def add_to_card(request, id):
    # Lấy sản phẩm cầm thêm vào card
    product = Product.objects.get(id=id)
    # Số sản phẩm thêm vào card khi chưa đăng nhập
    count_product = 1
    login = 0
    # Lấy user đã đăng nhập
    try:
        login_user = User.objects.get(username=request.user)
        login = 1
    except User.DoesNotExist:
        login = 0
    # Login = False thêm số lượng trả về JsonResponse. Thêm số lượng khi đã đăng nhập (Sử dụng ajax base.html)
    # Login = True thêm số lượng trả về redirect. Thêm số lượng khi chưa đăng nhập rồi yêu cầu đăng nhập mới cho add

    if request.method == 'POST':
        # Số sản phẩm thêm vào card khi đã đăng nhập
        count_product = int(request.POST.get('count'))

    # Lấy giá sale nếu cố
    try:     
        discount = product.discount.discount
    except AttributeError:
        discount = 0

    try:
        # Kiểm tra đã có đơn hàng thuộc user đăng nhập, với trạng thái chưa hoàn thành đơn nếu có
        # Kiểm tra tiếp
        order_old = Order.objects.get(user=login_user,status_id = 1)
        try:
            # Nếu đã có đơn hàng kiểm tra trong đơn hàng có sản phẩm nếu có
            # Tăng số lượng trong đơn hàng, thay đổi giá tổng
            product_add  = Chitietdonhang.objects.get(order=order_old, product=product)
            if product_add.soluong + count_product > product.soluong:
                if login == 1:
                    return JsonResponse({
                        'message': f'Số Lượng Sản Phẩm Vượt Quá'
                    }, status = 302)
                else:
                    return redirect('cart_url')
            else:
                product_add.soluong += count_product
            product_add.money = product_add.soluong*(product.price*(100-discount)/100)
            product_add.save()

        # Nếu đã có đơn hàng kiểm tra trong đơn hàng có sản phẩm nếu chưa
        # Thêm sản phẩm vào đơn hàng
        except Chitietdonhang.DoesNotExist:
            Chitietdonhang.objects.create(order=order_old, product=product, soluong=count_product, money = (product.price*(100-discount)/100)*count_product)
    
    # Kiểm tra đã có đơn hàng thuộc user đăng nhập, với trạng thái chưa hoàn thành đơn nếu chưa
    # Tạo đơn hàng
    except Order.DoesNotExist:
        order_new = Order.objects.create(status_id = 1, user=login_user)
        Chitietdonhang.objects.create(order=order_new, product=product, soluong=count_product, money = (product.price*(100-discount)/100)*count_product)

    if login == 1:
        return JsonResponse({
                    'message': f'Thêm Thành Công Sản Phẩm {product.name}'
                }, status = 200)
    else:
        return redirect('cart_url')
## Add product bằng button add end

## Xử lý register start
def register(request):
    if request.user.is_authenticated:
        logout(request)
    categories = Category.objects.all()
    type = Loai.objects.all()
    form = RegisterForm
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_user_url')
        else:
            return render(
                request=request,
                template_name= 'register.html',
                context= {
                    'categories': categories,
                    'types': type,
                    'form': form,
            }
    )
    return render(
        request=request,
        template_name= 'register.html',
        context= {
            'categories': categories,
            'types': type,
            'form': form,
        }
        
    )

def validation_username(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            User.objects.get(username=username)
            return JsonResponse({
                'message': f'Đã tồn tại {username}. Vui nhập username khác'
            }, status = 409)
        except User.DoesNotExist:
            space = 0
            for i in username:
                if i.isspace():
                    space += 1
            if space > 0:
                return JsonResponse({
                'message': 'Username không chứa khoảng trắng'
            }, status = 409)
            else:
                return JsonResponse({
                    'message': f'{username} Được sử dụng'
                }, status = 200)
            
def validation_password1(request):
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user)
            if check_password(password1,user.password):
                return JsonResponse({
                    'message': 'Mật khẩu trùng với mật khẩu cũ'
                }, status = 409)

        if len(password1) <= 8:
            return JsonResponse({
                'message': 'Mật khẩu có độ dài phải lớn hơn 8'
            }, status = 409)
        else:
            lower = 0
            upper = 0
            number = 0
            special = 0
            space = 0
            for i in password1:
                if i.isalpha():
                    if i.islower():
                        lower+=1
                    else:
                        upper+=1
                elif i.isdigit():
                    number+=1
                elif i.isspace():
                    space+=1
                else:
                    special+=1
            if lower == 0:
                return JsonResponse({
                'message': 'Mật khẩu chứa ký tự viết thường'
            }, status = 409)
            if upper == 0:
                return JsonResponse({
                'message': 'Mật khẩu chứa ký tự viết hoa'
            }, status = 409)
            if number == 0:
                return JsonResponse({
                'message': 'Mật khẩu chứa số'
            }, status = 409)
            if special == 0:
                return JsonResponse({
                'message': 'Mật khẩu chứa các ký tự đặc biệt'
            }, status = 409)
            if space > 0:
                return JsonResponse({
                'message': 'Mật khẩu không chứa khoảng trắng'
            }, status = 409)
            else:
                return JsonResponse({
                'message': ''
            }, status = 200)
            
def validation_password(request):
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            return JsonResponse({
                'message': 'Mật khẩu không trùng khớp'
            }, status = 409)
        else:
            return JsonResponse({
                'message': f'Mật khẩu trùng khớp'
            }, status = 200)
## Xử lý register end  

## Xử lý login, logout start
def login_user(request):
    if request.user.is_authenticated:
        return redirect('index_url')
    if request.method == 'POST':
        user = UserLoginForm(request.POST)
        if user.is_valid():
            user_login = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
            login(request, user_login)
            next = request.GET.get('next')
            if next:
                return redirect(next)
            return redirect('index_url')
        else:
            return render(
                request= request,
                template_name= 'login.html',
                context= {
                    'UserForm': user,
                }
            )
    return render(
        request=request,
        template_name='login.html',
        context={
            'UserForm': UserLoginForm,
        }
    )

def logout_user(request):
    logout(request)
    return redirect('index_url')
## Xử lý login, logout end

## Xử lý card start
@login_required(login_url='login_user_url')
def cart(request):
    categories = Category.objects.all()
    type = Loai.objects.all()
    sum_price = 0
    order_detail =""
    message = ""
    # Lấy user đang login
    login_user = User.objects.get(username=request.user)
    
    try:
        # Lấy ra đơn hàng thuộc user chưa thanh toán
        order = Order.objects.get(status_id = 1, user=login_user)
        # Lấy các sản phấm trong đơn hàng
        order_detail = Chitietdonhang.objects.filter(order=order)
        # Tính tổng tiền đơn hàng
        if order_detail:
            for product in order_detail:
                sum_price+=product.money

    except Order.DoesNotExist:
        order = ""
        message = "Chưa Có Đơn Hàng Nào"

    return render(
        request=request,
        template_name= 'cart.html',
        context= {
            'order_detail': order_detail,
            'categories': categories,
            'types': type,
            'total':sum_price,
            'message': message,
        }
    )

@login_required(login_url='login_user_url')
def remove_cart(request):
    if request.method == "GET":
        # Lấy id sản phẩm cần remove trong đơn hàng
        product = request.GET.get('remove')
    try:
        # Lấy user và đơn hang user
        login_user = User.objects.get(username=request.user)
        order = Order.objects.get(status_id = 1, user=login_user)

        # Lấy sản phẩm thuộc đơn hàng có id sản phẩm cần xóa
        order_detail = Chitietdonhang.objects.get(order = order, product_id = product)
        order_detail.delete()
        return redirect('cart_url')
    except Chitietdonhang.DoesNotExist:
        return redirect('cart_url')

@login_required(login_url='login_user_url')
def add_count_product(request):
    # Thay đổi số lượng sản phẩm trong cart = button +,-
    if request.method == "POST":
        # Lấy id, số lượng sản phẩm cần thay đổi trong đơn hàng
        count = int(request.POST.get('count'))
        product_id = request.POST.get('product_id')   
    try:
        # Lấy user login, order của user
        login_user = User.objects.get(username=request.user)
        order = Order.objects.get(status_id = 1, user=login_user)
        product = Product.objects.get(id = product_id)
        # Lấy sản phẩm thuộc đơn hàng
        order_detail = Chitietdonhang.objects.get(order = order, product_id = product_id)

        # Lấy ra sale của sản phẩm
        try:     
            discount = product.discount.discount
        except AttributeError:
            discount = 0

        # Thêm số lượng, giá mới vào DB
        order.soluong = count
        order.money = (product.price*(100-discount)/100)*count
        order.save()
        return JsonResponse({
            'message': 'Thay Đổi Số Lượng'
        }, status = 200)
    except Chitietdonhang.DoesNotExist:
        return JsonResponse({
            'message': 'Thêm Số Lượng Thất Bại'
        }, status = 302)
## Xử lý card end

## Xử lý checkout start
@login_required(login_url='login_user_url')
def checkout(request):
    categories = Category.objects.all()
    type = Loai.objects.all()
    user = User.objects.get(username=request.user)
    order_detail = ""
    sum_price = 0
    message = ""
    try:
        order = Order.objects.get(status=1, user=user)
        order_detail = Chitietdonhang.objects.filter(order=order)
        if order_detail:
            for product in order_detail:
                sum_price+=product.money

    except Order.DoesNotExist:
        message = "Chưa có sản phẩm trong đơn hàng"
    if order_detail:
        initial_dict = {
            "fullname" : user.fullname,
            "phone" : user.phone,
            "diachi": user.diachi,
            "email": user.email
        }

        form = OrderForm(initial= initial_dict)
        form_info =  OrderCreateForm(initial= initial_dict)

        if request.method == "POST":
            fullname = request.POST.get('fullname')
            phone = request.POST.get('phone')
            diachi = request.POST.get('diachi')
            email = request.POST.get('email')
            user.fullname = fullname
            user.phone = phone
            user.diachi = diachi
            user.email = email
            user.save()
            return redirect('checkout_url')
        
        return render(
            request=request,
            template_name= 'checkout.html',
            context= {
                'order_detail': order_detail,
                'categories': categories,
                'types': type,
                'total':sum_price,
                'form': form,
                'form_info': form_info,
                'message': message,
            }
        )
    else:
        return redirect('cart_url')

@login_required(login_url='login_user_url')
def confirm_order(request):
    if request.method == 'GET':
        # Lấy user login
        user = User.objects.get(username=request.user)
    try:
        # Lấy đơn hàng thuộc user với trạng thái chưa thanh toán
        order = Order.objects.get(user=user, status =1)
        # Lấy các sản phẩm thuộc đơn hàng
        order_detail = Chitietdonhang.objects.filter(order=order)

        # Thay đổi số lượng từng của sản phẩm khi thanh toán thành công
        for product_count in order_detail:
            product = Product.objects.get(id=product_count.product_id)
            soluong_old = product.soluong
            product_new = int(soluong_old) - int(product_count.soluong)
            # Nếu số lượng nhỏ < không hết hàng đặt số lượng = 0
            if product_new > 0:
                product.soluong = product_new
                product.save()
            else:
                product.soluong = 0
                product.save()
        else:
            # Khi thanh toán thành công tạo time đơn hàng thay đổi trạng thái
            order.status_id = 2
            order.date = datetime.now()
            order.save()
        return redirect('send_email_url')
    except Order.DoesNotExist:
        return redirect('cart_url')

@login_required(login_url='login_user_url')
def send_email(request):
    user = User.objects.get(username = request.user)
    try:
        order = Order.objects.get(user=user, status = 2)
        # Send Email Start
        order_detail = Chitietdonhang.objects.filter(order = order)
        subject = f"Thank You For {user.fullname}"
        message = "Đơn Hàng Đặt Mua Thành Công"
        sum_price = 0
        for product in order_detail:
            sum_price+=product.money
        html_content = loader.render_to_string(
            template_name= 'email.html',
            context={
                'message': message,
                'date': order.date.strftime("%Y/%m/%d %H:%M:%S"),
                'user': user,
                'order': order,
                'order_detail': order_detail,
                'price': sum_price,
                'sumprice': sum_price + 10000,
            }
        )
        email_form = settings.EMAIL_HOST_USER
        recipient_list = [user.email,]
        try:
            msg = EmailMultiAlternatives(subject, message, email_form, recipient_list)
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        except BadHeaderError:
            return render(
                request=request,
                template_name= '404.html'
            )
        # Send Email End
        order.status_id = 3
        order.save()
        return render(
            request=request,
            template_name= 'sendemail.html'
        )
    except Order.DoesNotExist:
        return redirect('cart_url')
## Xử lý checkout end

## Contact start
@login_required(login_url='login_user_url')
def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        email_form = settings.EMAIL_HOST_USER
        recipient_list = [email,]
        try:
            send_mail(subject, message, email_form, recipient_list)
        except BadHeaderError:
            return render(
                request=request,
                template_name= '404.html'
            )
    return render(
        request=request,
        template_name= 'contact.html',
        context= {
            'form' : ContactForm
        }
    )
## Contact End

## Error start
def error(request):
    return render(
        request=request,
        template_name= '404.html'
    )
## Error End

## ifomation start
@login_required(login_url='login_user_url')
def infomation(request):
    if request.user.is_authenticated:
        user = User.objects.get(username = request.user)
        initial_dict = {
            "fullname" : user.fullname,
            "phone" : user.phone,
            "diachi": user.diachi,
            "email": user.email,
        }
        message = ""
        orders = Order.objects.filter(user=user, status = 3).order_by('-date')
        if not orders:
            message = "Chưa Có Đơn Hàng Nào"
        form = OrderCreateForm(initial= initial_dict)
        if request.method == "POST":
            fullname = request.POST.get('fullname')
            phone = request.POST.get('phone')
            diachi = request.POST.get('diachi')
            email = request.POST.get('email')
            user.fullname = fullname
            user.phone = phone
            user.diachi = diachi
            user.email = email
            user.save()
            return redirect('Infomation_url')
    return render(
        request=request,
        template_name= 'infomation.html',
        context= {
            'form': form,
            'orders': orders,
            'message': message,
        }
    )
## infomation end

## change password start
@login_required(login_url='login_user_url')
def changepassword(request):
    if request.user.is_authenticated:
        user = User.objects.get(username = request.user)
        initial_dict_user = {
            "username": user.username
        }
        form_password = ChangePassword(initial=initial_dict_user)
        
        if request.method == "POST":
            initial_dict_user['password'] = request.POST.get('password')
            initial_dict_user['password1'] = request.POST.get('password1')
            initial_dict_user['password2'] = request.POST.get('password2')
            password = request.POST.get('password')
            if password:
                form_password = ChangePassword(data=initial_dict_user)
                if form_password.is_valid():
                    form_password.save()
                    return redirect('Infomation_url')
                else:
                    return render(
                        request=request,
                        template_name= 'changepassword.html',
                        context= {
                            'form_password': form_password
                })

        return render(
            request=request,
            template_name= 'changepassword.html',
            context= {
                'form_password': form_password
            }
        )
    
@login_required(login_url='login_user_url')
def validation_password_user(request):
    if request.user.is_authenticated:
        user = User.objects.get(username = request.user)
        if request.method == 'POST':
            password = request.POST.get('password')
            if not check_password(password,user.password):
                return JsonResponse({
                    'message': 'Mật khẩu không trùng khớp'
                }, status = 409)
            else:
                return JsonResponse({
                    'message': f'Mật khẩu trùng khớp'
                }, status = 200)
## change password End

## Detail Order Start
@login_required(login_url='login_user_url')
def detail_order(request,id):
    message = ""
    if request.user.is_authenticated:
        if request.method == 'GET':
            user = User.objects.get(username = request.user)
            order_detail = Chitietdonhang.objects.filter(order_id = id)
        if not order_detail:
            message = "Chưa Có Đơn Hàng Nào"

    return render(
        request=request,
        template_name= 'orderdetail.html',
        context= {
            'order_detail': order_detail,
            'message': message
        }
    )
## Detail Order End

## Rating Review Start
@login_required(login_url='login_user_url')
def review(request):
    if request.user.is_authenticated:
        user = User.objects.get(username = request.user)
        if request.method == 'POST':
            id = int(request.POST.get('id'))
            rating = request.POST.get('rating')
            review = request.POST.get('review')
            if rating:
                if rating.isdigit():
                    rating = int(rating)
            else:
                rating = 0
            try:
                product = Product.objects.get(id = id)
                Feedback.objects.create(user= user, product = product, vote = rating, content = review, date = timezone.now())
                return JsonResponse({
                    'message': 'Thành Công'
                }, status = 200)
            except Product.DoesNotExist:
                return JsonResponse({
                    'message': 'Thất Bại'
                }, status = 302)
## Rating Review End

## Forgot Password Start
def forgot_password(request):
    if request.method == "POST":
        print('oki')
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            user = User.objects.get(username = username)
            email = request.POST.get('email')
            token = default_token_generator.make_token(user)
            subject = 'Email Xác Nhận Quên Mật Khẩu'
            message = token
            email_form = settings.EMAIL_HOST_USER
            recipient_list = [email,]
            try:
                send_mail(subject, message, email_form, recipient_list)
                return redirect('confirm_token_password_url')
            except BadHeaderError:
                return render(
                    request=request,
                    template_name= '404.html'
                )
        else:
            return render(
                request=request,
                template_name= 'forgot_password.html',
                context= {
                    'form': form,
            }
        )
    return render(
        request=request,
        template_name= 'forgot_password.html',
        context= {
            'form': ForgotPasswordForm,
        }
    )

def confirm_token(request):
    if request.method == "POST":
        form = TokenPasswordForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'message': f'Đặt Mật Khẩu Mới Thành Công'
            }, status = 200)
        else:
            return render(
                request=request,
                template_name= 'confirm_token_password.html',
                context= {
                    'form': form,
                }
            )
    return render(
        request=request,
        template_name= 'confirm_token_password.html',
        context= {
            'form': TokenPasswordForm,
        }
    )

def validation_username_forgot_password(request):
    if request.method == "POST":
        username = request.POST.get('username')
        try:
            User.objects.get(username=username)
            return JsonResponse({
                'message': f'Tên Đăng Nhập Trùng Khớp'
            }, status = 200)
        except User.DoesNotExist:
            return JsonResponse({
                    'message': f'Tên Đăng Nhập Không Tồn Tại'
                }, status = 302)

def validation_email_forgot_password(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        try:
            user = User.objects.get(username=username)
            if user.email != email:
                return JsonResponse({
                    'message': f'Email xác nhận không chính xác'
                }, status = 302)
        except User.DoesNotExist:
            return JsonResponse({
                    'message': f'Tên Đăng Nhập Không Tồn Tại'
                }, status = 302)
        else:
            return JsonResponse({
                'message': f'Email trùng khớp'
            }, status = 200)
## Forgot Password End