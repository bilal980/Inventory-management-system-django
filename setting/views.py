from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from pathlib import Path
from django.contrib import messages
from account.forms import MyUserCreationForm
from django.views.generic import TemplateView, CreateView, ListView, DeleteView, UpdateView
from setting.models import BusinessDetail
from setting.forms import BusinessDetailForm
from account.models import MyUser


class SettingView(TemplateView):
    template_name = "setting.html"

    def get_context_data(self, **kwargs):
        context = super(SettingView, self).get_context_data(**kwargs)
        try:
            business_name = BusinessDetail.objects.all().last().Name
        except:
            business_name = 'Inventory Management System'
        try:
            business_logo = BusinessDetail.objects.all().last().logo
        except:
            business_logo = 'none'
        context.update({
            'business_name': business_name,
            'business_logo': business_logo
        })
        return context


class MyUserListView(ListView):
    model = MyUser
    paginate_by = 20
    template_name = "user.html"
    ordering = '-id'


def create_user(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            if email == None:
                messages.error(request, 'Please Provide Valid Email')
                return redirect(reverse_lazy('create_user'))
            password = request.POST.get('password')
            password2 = request.POST.get('password2')
            if password != password2:
                messages.error(request, 'Password Not match')
                return redirect(reverse_lazy('create_user'))
            user = MyUser.objects.create_user(email=email, password=password)
            user.save()
            if request.POST.get('username') is not None:
                user.name = request.POST.get('username')
                user.save()
            if request.POST.get('phone') is not None:
                user.phone = request.POST.get('phone')
                user.save()
            if request.FILES:
                img = request.FILES['picture']
                user.picture = img
                user.save()
            messages.success(request, 'User Created Successfully!')
            return redirect(reverse_lazy('user_setting'))
        except:
            messages.error(request, 'Some Error Occurred!')
            return redirect(reverse_lazy('create_user'))
    return render(request, 'create_user.html')


def MyUserUpdateView(request, pk):
    if request.method == 'POST':
        try:
            user = MyUser.objects.get(id=pk)
            if request.POST.get('password') is not None:
                user.set_password(request.POST.get('password'))
                user.save()
            if request.POST.get('email') is not None:
                user.email = request.POST.get('email')
                user.save()
            if request.POST.get('username') is not None:
                user.name = request.POST.get('username')
                user.save()
            if request.POST.get('phone') is not None:
                user.phone = request.POST.get('phone')
                user.save()
            if request.FILES:
                img = request.FILES['picture']
                user.picture = img
                user.save()
            messages.success(request, 'Updated Successfully!')
            return redirect(request.META['HTTP_REFERER'])
        except:
            messages.error(request, 'Some Error Occured!')
            return redirect(request.META['HTTP_REFERER'])
    user = MyUser.objects.get(id=pk)
    context = {'User': user}
    return render(request, 'update_user.html', context)


class MyUserCreateView(CreateView):
    model = MyUser
    form_class = MyUserCreationForm
    template_name = "create_user.html"

    def get_context_data(self, **kwargs):
        context = super(MyUserCreateView, self).get_context_data(**kwargs)
        emp = Employee.objects.all()
        context.update({'employe': emp})
        return context


class MyUserDeleteView(DeleteView):
    model = MyUser
    success_url = reverse_lazy('user_setting')

    def get(self, request, *args, **kwargs):
        messages.warning(self.request, 'User Deleted!')
        return self.delete(request, *args, **kwargs)


def save_general_setting(request):
    if request.method == 'POST':
        try:
            set_id = BusinessDetail.objects.all().last()
            bus_form = BusinessDetailForm(
                request.POST, request.FILES, instance=set_id)
            if bus_form.is_valid():
                messages.success(request, 'Setting Successfully Changed!')
                bus_form.save()
        except:
            messages.error(request, 'Some Error Occured!')

    return redirect('/setting/')


