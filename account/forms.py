from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from account.models import MyUser


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ('email', 'password')


class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = MyUser
        fields = ('email',)
