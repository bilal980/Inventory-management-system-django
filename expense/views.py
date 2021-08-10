from django.views.generic import ListView
from django.contrib import messages
from django.views.generic.edit import CreateView,DeleteView,UpdateView
from expense.models import ExtraExpense
from expense.forms import ExtraExpenseForm
from django.urls import reverse_lazy

class ExtraExpenseListView(ListView):
    model = ExtraExpense
    template_name = "expense_list.html"
    paginate_by=40
    ordering='-id'
    
    def get_queryset(self):
        queryset = ExtraExpense.objects.all().order_by('-date')
        return queryset

class ExtraExpenseCreateView(CreateView):
    form_class = ExtraExpenseForm
    template_name = "add_expense.html"
    success_url = reverse_lazy("expense_list")

    def form_valid(self, form):
        messages.success(self.request, 'Expenese Created!')
        return super().form_valid(form)

class ExtraExpenseDeleteView(DeleteView):
    model = ExtraExpense
    template_name = "expense_list.html"
    success_url = reverse_lazy("expense_list")

    def get(self, request, *args, **kwargs):
        messages.warning(self.request,'Expense Record Deleted!')
        return self.post(request, *args, **kwargs)

class ExtraExpenseUpdateView(UpdateView):
    model=ExtraExpense
    template_name = 'update_expense.html'
    form_class=ExtraExpenseForm
    success_url='/expense/'

    def form_valid(self, form):
        messages.success(self.request, 'Expenese Updated!')
        return super().form_valid(form)


