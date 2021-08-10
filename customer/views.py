from customer.models import Customer
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView,DeleteView
from django.views.generic import ListView
from django import forms
from .forms import CustomerForm

class CustomerCreateView(CreateView):
    form_class = CustomerForm
    template_name = "add_customer.html"
    success_url = '/customer/'

    def form_valid(self,form):
        messages.success(self.request,'Customer Added!')
        return super().form_valid(form)

class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = "update_customer.html"
    success_url = '/customer/'

    def form_valid(self, form):
        messages.success(self.request, 'Customer Updated Successfully!')
        return super().form_valid(form)
  
class CustomerListView(ListView):
    model = Customer
    template_name = "customer.html"
    paginate_by = 40
    ordering = ('customer_name',)

class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = "customer.html"
    success_url=reverse_lazy('customer')
    def get(self,request,*args,**kwargs):
        messages.warning(self.request,'Customer Deleted!')
        return self.delete(request,*args,**kwargs)


    

    
