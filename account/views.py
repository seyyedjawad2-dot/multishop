
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from .forms import LoginForm, RegisterForm, OTPForm
from .models import User
from django.core.mail import send_mail
from django.conf import settings
import random
from .models import EmailOTP


class UserLogin(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['email'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                form.add_error("email", "invalid user data")
        else:
            form.add_error("password", "invalid data")
        return render(request, 'account/login.html', {'form': form})


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, "account/register.html", {"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            request.session["email"] = email
            request.session["password"] = password
            code = str(random.randint(1000, 9999))
            EmailOTP.objects.create(
                email=email,
                code=code,
                is_used=False
            )

            send_mail(
                subject="کد تایید ثبت نام",
                message=f":کد شما{code}\n این کد یک دقیقه اعتبار دارد ",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
            return redirect("account:verify")
        return render(request, "account/register.html", {"form": form})


class VerifyView(View):
    def get(self, request):
        form = OTPForm()
        return render(request, "account/verify.html", {"form": form})
    def post(self, request):
        form = OTPForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]
            email = request.session.get("email")
            password = request.session.get("password")
            if not email or not password:
                return redirect('register')

            otp_record = EmailOTP.objects.filter(email=email, code=code, is_used=False).last()

            if not otp_record:
                    form.add_error('code','کد اشتباه')
                    return render(request, "account/verify.html", {"form": form})
            if otp_record.is_expired():
                    form.add_error('code', "کد منقضی شده")

                    return render(request, 'account/verify.html', {'form': form})
            user = User.objects.create_user(email=email, password=password)


            login(request, user,)
            otp_record.is_used = True
            otp_record.save()
            del request.session["email"]
            del request.session["password"]
            return redirect("/")
        return render(request, 'account/verify.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect("/")