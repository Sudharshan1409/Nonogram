from django.shortcuts import render, redirect, reverse
from django.views.generic import View, CreateView
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib import messages
from nonogram.settings import EMAIL_HOST_USER, SECRET_KEY
from user.decorators import should_not_be_logged_in
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserForm
from jwt import encode as jwt_encode, decode as jwt_decode
from django.shortcuts import get_object_or_404
from .forms import LoginForm
from django.contrib.auth.views import LoginView
from user.auth import login_user

# Create your views here.


@method_decorator(should_not_be_logged_in, name='dispatch')
class ResetPasswordView(View):

    def get(self, request):
        if request.GET.get('token'):
            token = request.GET.get('token')
            print('token', token)
            try:
                decoded = jwt_decode(
                    token, SECRET_KEY, algorithms=['HS256'])
                return render(request, 'user/change_password.html', decoded)
                print('decoded', decoded)
            except:
                messages.warning(request, 'Invalid token')
                return redirect(reverse('user:password_reset'))
        return render(request, 'user/reset_password.html')

    def post(self, request):
        if request.POST.get('password1'):
            if request.POST.get('password1') == request.POST.get('password2'):
                user = get_user_model().objects.get(id=request.POST.get('userId'))
                user.set_password(request.POST.get('password1'))
                user.save()
                messages.success(request, 'Password Reset successfully')
                return redirect(reverse('user:login'))
            else:
                messages.warning(request, 'Password do not match')
                return redirect(reverse('user:password_reset'))
        else:
            user = get_object_or_404(get_user_model(), email=request.POST.get('email'))
            if not user:
                messages.warning(request, 'User with Email not found')
                return redirect(reverse('user:password_reset'))
            token = jwt_encode({"email": request.POST.get(
                'email'), "userId": user.id}, SECRET_KEY, algorithm="HS256")
            print('token', token)
            if user:
                send_mail(
                    'Password Reset',
                    f'''
                    Hi {user.name},
                    Reset password by clicking here: {request.build_absolute_uri()}?token={token}
                    ''',
                    EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )
                messages.success(
                    request, 'Password reset link sent to your email')
                return redirect(reverse('user:login'))
            else:
                messages.warning(request, 'Email not found')
                return redirect(reverse('user:password_reset'))


class ChangePasswordView(LoginRequiredMixin, View):
    template_name = 'user/change_password.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        if request.POST.get('password1') == request.POST.get('password2'):
            user = get_user_model().objects.get(id=request.user.id)
            user.set_password(request.POST.get('password1'))
            user.save()
            messages.success(request, 'Password changed successfully')
            user = authenticate(
                request, email=request.user.email, password=request.POST.get('password1'))
            login_user(request, user)
            return redirect(reverse('home'))
        else:
            messages.warning(request, 'Password do not match')
            return redirect(reverse('user:password_change'))


@ method_decorator(should_not_be_logged_in, name='dispatch')
class RegisterUserView(CreateView):
    template_name = 'user/register.html'
    context_object_name = 'form'
    model = get_user_model()
    form_class = UserForm

    def get_success_url(self):
        return reverse('home')

    def form_valid(self, form):
        # Save the new user first
        user = form.save()

        # Authenticate the user using the provided email and password
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        user = authenticate(email=email, password=password)
        if user is not None:
            # Log the user in
            login_user(self.request, user)
            return redirect(self.get_success_url())

        # If authentication failed, you might want to handle it (though it shouldn't fail in this scenario)
        return super().form_invalid(form)


@method_decorator(should_not_be_logged_in, name='dispatch')
class LoginView(LoginView):
    template_name = 'user/login.html'
    authentication_form = LoginForm


