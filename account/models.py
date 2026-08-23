from datetime import timedelta
from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
from django.utils import timezone


class  UserManager(BaseUserManager):
    def create_user(self,email, password=None):
      if not email:
        raise ValueError("Users must have an email address")
      user = self.model(email=self.normalize_email(email))
      user.set_password(password)
      user.save(using=self._db)
      return user

    def create_superuser(self , email, password=None):
        user= self.create_user( email , password=password,)
        user.is_admin=True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):

    email=models.EmailField(
        verbose_name="ایمیل",
        max_length=55,
        unique=True,
        null=True,
    )
    fullname = models.CharField(max_length=50,verbose_name="نام کامل",null=True,blank=True)
    is_active=models.BooleanField(default=True,verbose_name="فعال")
    is_admin=models.BooleanField(default=True,verbose_name="ادمین")


    objects = UserManager()

    USERNAME_FIELD="email"
    REQUIRED_FIELDS=[]


    class Meta:
        verbose_name= "کاربر"
        verbose_name_plural= "کاربرها"


    def __str__(self):
        return self.email
    def has_perm(self,perm,obj=None):
        return True
    def has_module_perms(self,app_label):
        return True
    @property
    def is_staff(self):
        return self.is_admin



class EmailOTP(models.Model):
    email = models.EmailField(verbose_name='ایمیل شما')
    code = models.CharField(max_length=6,verbose_name='کد یکبار مصرف')
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=2)