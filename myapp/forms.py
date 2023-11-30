from django.contrib.auth import get_user_model, authenticate, login
User = get_user_model()
from .models import ThanhPho, QuanHuyen, PhuongXa
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.tokens import default_token_generator  

class RegisterForm(forms.Form):
    months={
        1:'Tháng 1',
        2:'Tháng 2',
        3:'Tháng 3',
        4:'Tháng 4',
        5:'Tháng 5',
        6:'Tháng 6',
        7:'Tháng 7',
        8:'Tháng 8',
        9:'Tháng 9',
        10:'Tháng 10',
        11:'Tháng 11',
        12:'Tháng 12',
    }
    username = forms.CharField(
        label='Tên đăng nhập',
        max_length=100,
        min_length=8,
        widget=forms.TextInput(attrs = {"class":"form-control", "autocomplete":"off !important", "value":""})
    )
    password1 = forms.CharField(
        label='Mật khẩu',
        max_length=50,
        min_length=8,
        help_text= ["Mật khẩu của bạn phải chứa ít nhất 8 ký tự.","Mật khẩu của phải có số.", "Mật khẩu của bạn chứa ký tự viết hoa.", "Mật khẩu của bạn chứa ký tự đặc biệt.(@,#,%...)"],
        widget=forms.PasswordInput(attrs = {"class":"form-control", "autocomplete":"off !important", "value":""}),
    )
    password2 = forms.CharField(
        label='Xác nhận mật khẩu',
        max_length=50,
        min_length=8,
        widget=forms.PasswordInput(attrs =  {"class":"form-control"})
        )
    
    fullname = forms.CharField(
        label='Họ và Tên',
        max_length=100,
        widget=forms.TextInput(attrs = {"class":"form-control"})
        )
    
    firstname = forms.CharField(
        label='Họ',
        max_length=100,
        widget=forms.TextInput(attrs = {"class":"form-control"})
    )

    lastname = forms.CharField(
        label='Tên',
        max_length=100,
        widget=forms.TextInput(attrs = {"class":"form-control"})
    )

    ngaysinh = forms.DateField(
        label='Ngày Sinh',
        widget=forms.SelectDateWidget(attrs = {"class":"form-select"},years=range(1900, 2024), months=months)
    )

    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs = {"class":"form-control"})
    )
    phone = forms.CharField(
        label='Số Điện Thoại',
        max_length=15,
        widget=forms.TextInput(attrs = {"class":"form-control"})
    )

    diachi = forms.CharField(
        label='Địa Chỉ',
        max_length=255,
        widget=forms.TextInput(attrs = {"class":"form-control"})
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
            raise ValidationError(f'Đã tồn tại {username}. Vui nhập username khác')
        except User.DoesNotExist:
            space = 0
            for i in username:
                if i.isspace():
                    space += 1
            if space > 0:
                raise ValidationError('Username không chứa khoảng trắng')
            else:
                return username
    
    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if len(password1) <= 8:
            self._errors['password1'] = self.error_class([
                'Mật khẩu có độ dài phải lớn hơn 8'])
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
                self._errors['password1'] = self.error_class([
                    'Mật khẩu phải có ký tự viết thường'])
            elif upper == 0:
                self._errors['password1'] = self.error_class([
                    'Mật khẩu phải có ký tự viết hoa'])
            elif number == 0:
                self._errors['password1'] = self.error_class([
                    'Mật khẩu phải có số'])
            elif space > 0:
                self._errors['password1'] = self.error_class([
                    'Mật khẩu không chứa khoảng trắng'])
            elif special == 0:
                self._errors['password1'] = self.error_class([
                    'Mật khẩu phải bao gồm 1 ký tự đặc biệt'])

        if password1 != password2:
            self._errors['password2'] = self.error_class([
                'Mật khẩu không đúng. Vui lòng nhập lại'])
        return self.cleaned_data
   
    def save(self):
        return User.objects.create_user(
            username = self.cleaned_data['username'],
            password = self.cleaned_data['password1'],
            fullname = self.cleaned_data['fullname'],
            first_name = self.cleaned_data['firstname'],
            last_name = self.cleaned_data['lastname'],
            ngaysinh = self.cleaned_data['ngaysinh'],
            email = self.cleaned_data['email'],
            phone = self.cleaned_data['phone'],
            diachi = self.cleaned_data['diachi'],
            save_password = self.cleaned_data['password1'],
        )
    
class UserLoginForm(forms.Form):
    username = forms.CharField(
        label='Tên Đăng Nhập',
        max_length=255,
        widget=forms.TextInput(attrs = {"class":"form-control"})
    )
    password = forms.CharField(
        label='Mật Khẩu',
        max_length=255,
        widget=forms.PasswordInput(attrs = {"class":"form-control"})
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username is not None and password:
            login = authenticate(username=username, password=password)
            if login is None:
                raise ValidationError('Thông Tin Đăng Nhập Sai')
        return self.cleaned_data

class ChangePassword(forms.Form):
    username = forms.CharField(
        label='Tên Đăng Nhập',
        max_length=255,
        widget=forms.TextInput(attrs = {"class":"form-control", "disabled":""})
    )
    password = forms.CharField(
        label='Mật Khẩu Cũ',
        max_length=50,
        min_length=8,
        widget=forms.PasswordInput(attrs =  {"class":"form-control"})
        )

    password1 = forms.CharField(
        label='Mật khẩu mới',
        max_length=50,
        min_length=8,
        help_text= ["Mật khẩu của bạn phải chứa ít nhất 8 ký tự.","Mật khẩu của phải có số.", "Mật khẩu của bạn chứa ký tự viết hoa.", "Mật khẩu của bạn chứa ký tự đặc biệt.(@,#,%...)"],
        widget=forms.PasswordInput(attrs = {"class":"form-control",}),
    )
    password2 = forms.CharField(
        label='Xác nhận mật khẩu',
        max_length=50,
        min_length=8,
        widget=forms.PasswordInput(attrs =  {"class":"form-control"})
        )

    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = User.objects.get(username=username)
        if not check_password(password,user.password):
            raise ValidationError(f'Mật Khẩu Không Đúng')
        else:
            return username
        
    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        username = self.cleaned_data.get('username')
        user = User.objects.get(username=username)
        if check_password(password1,user.password):
            self._errors['password1'] = self.error_class([
                'Mật khẩu trùng với mật khẩu cũ'])
 
        if len(password1) <= 8:
            self._errors['password1'] = self.error_class([
                'Mật khẩu có độ dài phải lớn hơn 8'])
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
                self._errors['password1'] = self.error_class([
                    'Mật khẩu phải có ký tự viết thường'])
            elif upper == 0:
                self._errors['password1'] = self.error_class([
                    'Mật khẩu phải có ký tự viết hoa'])
            elif number == 0:
                self._errors['password1'] = self.error_class([
                    'Mật khẩu phải có số'])
            elif space > 0:
                self._errors['password1'] = self.error_class([
                    'Mật khẩu không chứa khoảng trắng'])
            elif special == 0:
                self._errors['password1'] = self.error_class([
                    'Mật khẩu phải bao gồm 1 ký tự đặc biệt'])

        if password1 != password2:
            self._errors['password2'] = self.error_class([
                'Mật khẩu không đúng. Vui lòng nhập lại'])
        return self.cleaned_data
    
    def save(self):
        username = self.cleaned_data.get('username')
        user = User.objects.get(username=username)
        user.set_password(self.cleaned_data['password1'])
        user.save_password = self.cleaned_data['password1']
        user.save()

class OrderForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['fullname', 'phone', 'diachi', 'email']
        widgets = {
            'fullname': forms.TextInput(attrs = {"class":"form-control", "disabled":""}),
            'phone': forms.TextInput(attrs = {"class":"form-control", "disabled":""}),
            'diachi': forms.TextInput(attrs = {"class":"form-control ", "disabled":""}),
            'email': forms.TextInput(attrs= {"class":"form-control", "disabled":""}),
        }
        labels = {
            'fullname': 'Họ và Tên:',
            'phone': 'Số Điện Thoại:',
            'diachi': 'Địa Chi:',
            'email': 'Email:',
        }

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['fullname', 'phone', 'diachi', 'email']
        widgets = {
            'fullname': forms.TextInput(attrs = {"class":"form-control"}),
            'phone': forms.TextInput(attrs = {"class":"form-control"}),
            'diachi': forms.TextInput(attrs = {"class":"form-control "}),
            'email': forms.TextInput(attrs= {"class":"form-control"}),
        }
        labels = {
            'fullname': 'Họ và Tên:',
            'phone': 'Số Điện Thoại:',
            'diachi': 'Địa Chi:',
            'email': 'Email:',
        }

class ContactForm(forms.Form):
    name = forms.CharField(
        label='Tên',
        max_length=255,
        widget=forms.TextInput(attrs = {"class":"form-control", "placeholder":"Your Name"})
    )
    email = forms.EmailField(
        label='Email',
        max_length=50,
        min_length=8,
        widget=forms.EmailInput(attrs =  {"class":"form-control", "placeholder":"Your Email"})
        )

    subject = forms.CharField(
        label='Subject',
        widget=forms.TextInput(attrs = {"class":"form-control", "placeholder":"Subject"}),
    )
    message = forms.CharField(
        label='Message',
        max_length=255,
        min_length=8,
        widget=forms.Textarea(attrs =  {"class":"form-control", "placeholder":"Message"})
        )
    
class ForgotPasswordForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs = {"class":"form-control"}),
            'email': forms.TextInput(attrs= {"class":"form-control"}),
        }
        labels = {
            'username': 'Tên Đăng Nhập:',
            'email': 'Email:',
        }
    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        try:
            user = User.objects.get(username=username)
            if user.email != email:
                self._errors['email'] = self.error_class([
                'Email xác nhận không chính xác'])
        except User.DoesNotExist:
            self._errors['username'] = self.error_class([
                'Tên Đăng Nhập Không Tồn Tại'])
        return self.cleaned_data


class TokenPasswordForm(forms.Form):
    username = forms.CharField(
        label='Tên Đăng Nhập',
        max_length=255,
        widget=forms.TextInput(attrs =  {"class":"form-control", "placeholder":"Tên Đăng Nhập", 'required':''})
        )
    token = forms.CharField(
        label='Mã Xác Nhận',
        max_length=255,
        help_text= ["Mã Xác Nhận Đã Được Gửi Tới Email"],
        widget=forms.TextInput(attrs = {"class":"form-control", "placeholder":"Mã Xác Nhận", 'required':''})
    )
    password1 = forms.CharField(
        label='Mật khẩu mới',
        max_length=50,
        min_length=8,
        help_text= ["Mật khẩu của bạn phải chứa ít nhất 8 ký tự.","Mật khẩu của phải có số.", "Mật khẩu của bạn chứa ký tự viết hoa.", "Mật khẩu của bạn chứa ký tự đặc biệt.(@,#,%...)"],
        widget=forms.PasswordInput(attrs = {"class":"form-control","placeholder":"Mật Khẩu Mới",'required':''}),
    )
    password2 = forms.CharField(
        label='Xác nhận mật khẩu',
        max_length=50,
        min_length=8,
        widget=forms.PasswordInput(attrs =  {"class":"form-control","placeholder":"Xác nhận mật khẩu", 'required':''})
        )
    
    def clean(self):
        username = self.cleaned_data.get('username')
        token = self.cleaned_data.get('token')
        try:
            user = User.objects.get(username=username)
            if not default_token_generator.check_token(user, token):
                self._errors['token'] = self.error_class([
                'Mã Xác Nhận Không Chính Xác'])
        except User.DoesNotExist:
            self._errors['username'] = self.error_class([
                'Tên Đăng Nhập Không Tồn Tại'])
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1:
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
                self._errors['password1'] = self.error_class([
                    'Mật khẩu phải có ký tự viết thường'])
            elif upper == 0:
                self._errors['password1'] = self.error_class([
                    'Mật khẩu phải có ký tự viết hoa'])
            elif number == 0:
                self._errors['password1'] = self.error_class([
                    'Mật khẩu phải có số'])
            elif space > 0:
                self._errors['password1'] = self.error_class([
                    'Mật khẩu không chứa khoảng trắng'])
            elif special == 0:
                self._errors['password1'] = self.error_class([
                    'Mật khẩu phải bao gồm 1 ký tự đặc biệt'])

        if password1 != password2:
            self._errors['password2'] = self.error_class([
                'Mật khẩu không đúng. Vui lòng nhập lại'])
        return self.cleaned_data
    
    def save(self):
        username = self.cleaned_data.get('username')
        user = User.objects.get(username=username)
        user.set_password(self.cleaned_data['password1'])
        user.save_password = self.cleaned_data['password1']
        user.save()