from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", index, name="index"),
    path("services/", services, name="services"),
    path("ride/", ride, name="ride"),
    path("contactus/", contactus, name="contactus"),
    path("about/", about, name="about"),
    path("review/", review, name="review"),
    path("policy/", policy, name="policy"),
    path("risk/", risk, name="risk"),
    path("terms/", terms, name="terms"),
    path("home/",home,name="home"),
    path("add/", add, name="add"),
    path('edit/<id>',edit,name="edit"),
    path("delete/<int:id>", delete_data, name="delete_data"),
    path("clear/", clear_items, name="clear_items"),
    path("recycle/", recycle, name="recycle"),
    path("restore/<int:id>", restore, name="restore"),
    path("payment/", payment, name="payment"),
    # "------------------------------------------------------------""------------------------------------------------------------""------------------------------------------------------------"
    # "------------------------------------------------------------""------Auth------------------------------------------------------"
    path("log_in/", log_in, name="log_in"),
    path('log_out/',auth_views.LogoutView.as_view(), name='log_out'),
    path("register/", register, name="register"),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='auth/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'),name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'), name='password_reset_complete'),
]
