from django.urls import path
from .views import RegisterUserView, ResetPasswordView, ChangePasswordView, LoginView
from django.contrib.auth.views import LogoutView

app_name = 'user'

urlpatterns = [
    path('signup/', RegisterUserView.as_view(), name='signup'),
    path('password/reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password/change/', ChangePasswordView.as_view(), name='password_change'),
    path('login/', LoginView.as_view(), name="login", kwargs={'next_page': '/'}),
    path('logout/', LogoutView.as_view(), name='logout'),
]
