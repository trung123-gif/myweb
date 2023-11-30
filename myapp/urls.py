from django.urls import path
from . import views
urlpatterns = [
    # Trang Chủ
    path(route='', view=views.index, name = 'index_url'),

    # Trang Views
    path(route='views/', view=views.views, name = 'views_url'),

    # Trang Detail
    path(route='views/detail/<int:id>', view=views.detail, name = 'detail_url'),
    
    # Xử lý card
    path(route='cart/', view=views.cart, name = 'cart_url'),
    path(route='remove_cart/', view=views.remove_cart, name = 'remove_cart_url'),
    path(route='add_count_product/', view=views.add_count_product, name = 'add_count_product_url'),

    # Add product bằng button add start
    path(route='addtocard/<int:id>', view=views.add_to_card, name = 'add_to_cart_url'),

    # Xử lý register start
    path(route='register/', view=views.register, name = 'register_url'),
    path(route='validation_username/', view=views.validation_username, name = 'validation_username_url'),
    path(route='validation_password/', view=views.validation_password, name = 'validation_password_url'),
    path(route='validation_password1/', view=views.validation_password1, name = 'validation_password1_url'),

    # Xử lý login, logout
    path(route='login/', view=views.login_user, name = 'login_user_url'),
    path(route='logout/', view=views.logout_user, name = 'logout_user_url'),

    # Xử lý checkout
    path(route='checkout/', view=views.checkout, name = 'checkout_url'),
    path(route='checkout/confirm_order/', view=views.confirm_order, name = 'confirm_order_url'),
    path(route='checkout/confirm_order/sendemail', view=views.send_email, name = 'send_email_url'),

    # Contact start
    path(route='contact/', view=views.contact, name = 'contact_url'),

    # Error start
    path(route='error/', view=views.error, name = 'error_url'), 

    # Infomation start
    path(route='infomation/', view=views.infomation, name = 'Infomation_url'), 

    # Change Password start
    path(route='infomation/changepassword/', view=views.changepassword, name = 'changepassword_url'), 

    # Validation Change Password start
    path(route='validation_password_user/', view=views.validation_password_user, name = 'validation_password_user_url'),

    # Detail Order
    path(route='infomation/order/<int:id>', view=views.detail_order, name = 'detail_order_url'), 

    # Detail Order
    path(route='reviews', view=views.review, name = 'reviews_url'), 

    # Forgot Password
    path(route='forgotpassword/', view=views.forgot_password, name = 'forgot_password_url'), 
    path(route='validation_username_forgotpassword/', view=views.validation_username_forgot_password, name = 'validation_username_forgot_password_url'), 
    path(route='validation_email_forgotpassword/', view=views.validation_email_forgot_password, name = 'validation_email_forgot_password_url'), 
    path(route='forgotpassword/confirm', view=views.confirm_token, name = 'confirm_token_password_url'), 
]