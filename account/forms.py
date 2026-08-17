from django import forms
from django.core import validators

from .models import  User
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError



class UserCreationForm(forms.ModelForm):

    password1=forms.CharField(label="گذرواژه",widget=forms.PasswordInput)
    password2=forms.CharField(label="تکرار گذرواژه",widget=forms.PasswordInput)

    class Meta:
       model=User
       fields=["email",]


    def clean_password2( self):
        password1 = self.cleaned_data.get("password1")
        password2= self.cleaned_data.get("password2")

        if password1 and password2 and password1!=password2:
            raise ValidationError("Passwords don't match")
        return password2



    def save(self,commit=True):

        user=super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit :
         user.save()
        return user



class UserChangeForm(forms.ModelForm):

    password=ReadOnlyPasswordHashField()
    class Meta:
        model=User
        fields=("email","password","is_active","is_admin")




class LoginForm(forms.Form):
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))


class RegisterForm(forms.Form):
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def clean_email(self):
        email=self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already registered")
        return email



class OTPForm(forms.Form):
    code=forms.CharField(max_length=4,widget=forms.TextInput(attrs={'class':'form-control'}))

    def clean_code(self):
        code=self.cleaned_data.get("code")
        if not code.isdigit():
            raise forms.ValidationError('only numbers')
        return code