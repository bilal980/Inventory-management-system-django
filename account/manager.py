from django.contrib.auth.models import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class MyUserManager(BaseUserManager):
    def create_user(self, email, password,**kwargs):
        if not email:
            raise ValueError(_('Email is Required!'))
        em = self.normalize_email(email)
        user = self.model(email=em)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,password,**kwargs):
        user = self.create_user(email=email,password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser=True
        
        if user.is_staff!= True:
            raise ValueError("Is_staff must be True")
        user.save(using=self._db)
        return user
