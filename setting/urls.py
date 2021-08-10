from django.urls import path
from setting import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', login_required(views.SettingView.as_view(),login_url='/'), name='general_setting'),
    path('general/', login_required(views.save_general_setting,login_url='/'), name='save_general_setting'),
    path('user/', login_required(views.MyUserListView.as_view(),login_url='/'), name='user_setting'),
    path('user/create/', login_required(views.create_user,login_url='/'), name='create_user'),
    path('user/delete/<int:pk>', login_required(views.MyUserDeleteView.as_view(), login_url='/'), name='delete_user'),
    path('user/update/<int:pk>', login_required(views.MyUserUpdateView, login_url='/'), name='update_user'),
    path('profile/', login_required(views.MyUserListView.as_view(),login_url='/'), name='profile_setting'),
    path('update/profile/<int:pk>', login_required(views.MyUserUpdateView,login_url='/'), name='update_profile'),
]
