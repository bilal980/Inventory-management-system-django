from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from account.manager import MyUserManager
# Create your models here.


class DatedModel(models.Model):
    class Meta:
        abstract = True
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='Email', max_length=60, unique=True)
    name=models.CharField(max_length=40,null=True,blank=True)
    phone=models.IntegerField(null=True,blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    picture = models.ImageField(upload_to='static/image/profile_pic/', null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = MyUserManager()

    def __str__(self):
        return self.email


    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True