from django.shortcuts import redirect, HttpResponseRedirect
from django.contrib import messages
from django.urls import resolve
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic import ListView, TemplateView, FormView, UpdateView
from employe.models import Employee, EmployeeSalary
from employe.forms import EmployeeForm, EmployeeSalaryForm
from django.urls import reverse_lazy,reverse

# Create your views here.
class EmployeCreateView(CreateView):
    form_class = EmployeeForm
    template_name = "add_employe.html"
    success_url = '/employe/'

    def form_valid(self, form):
        messages.success(self.request, 'Employe Added!')
        return super().form_valid(form)

class EmployeeListView(ListView):
    model = Employee
    template_name = "employe.html"
    paginate_by = 40
    ordering = ['name']

class EmployeeDeleteView(DeleteView):
    model = Employee
    success_url = '/employe/'

    def get(self, request, *args, **kwargs):
        messages.warning(self.request,'Employe Deleted!')
        return self.post(request, *args, **kwargs)

class EmployeeSalaryCreateView(FormView):
    form_class = EmployeeSalaryForm
    template_name = 'add_salary.html'

    def form_valid(self, form):
        obj = form.save()
        obj.employee = Employee.objects.get(
            name=self.request.POST.get('employee_name'))
        obj.save()
        messages.success(self.request,'Salary Recorded!')
        return HttpResponseRedirect(reverse('detail_salary', args=[self.kwargs.get('pk')]))

    def form_invalid(self, form):
        return super(EmployeeSalaryCreateView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(EmployeeSalaryCreateView,
                        self).get_context_data(**kwargs)
        employee = (
            Employee.objects.get(id=self.kwargs.get('pk'))
        )
        context.update({
            'employee': employee
        })
        return context

class EmployeeSalaryDetailView(ListView):
    model=EmployeeSalary
    paginate_by=20
    template_name = 'detail_salary.html'
    ordering='-id'

    def get_context_data(self, **kwargs):
        context = super(
            EmployeeSalaryDetailView, self).get_context_data(**kwargs)

        try:
            salaries = EmployeeSalary.objects.filter(
                employee__id=self.kwargs.get('pk')
            )
        except Employee.DoesNotExist:
            raise Http404

        context.update({
            'salaries': salaries,
            'employee': Employee.objects.get(id=self.kwargs.get('pk'))

        })

        return context

class EmployeeUpdateView(UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = "update_employe.html"
    success_url='/employe/'

    def form_valid(self, form):
        messages.success(self.request, 'Employe Updated Successfully!')
        return super().form_valid(form)

class EmployeeSalaryDeleteView(DeleteView):
    model = EmployeeSalary
    template_name = "detail_salary.html"

    def get(self,request,*args,**kwargs):        
        self.success_url =request.META['HTTP_REFERER']
        messages.warning(self.request,'Salary Record Deleted!')
        return self.delete(request,*args,**kwargs)

