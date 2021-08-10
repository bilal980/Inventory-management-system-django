from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
from supplier.models import SupplierStatement, Supplier
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView,DeleteView
from django.views.generic import ListView
from supplier.forms import AddSupplierForm, SupplierStatementForm
from django.db.models import Sum

class SupplierCreateView(CreateView):
    form_class = AddSupplierForm
    template_name = "add_supplier.html"
    success_url = reverse_lazy('supplier')
    
    def form_valid(self, form):
        messages.success(self.request, 'Supplier Added!')
        return super().form_valid(form)

class SupplierListView(ListView):
    model = Supplier
    template_name = "list_supplier.html"
    paginate_by = 40
    ordering='-id'

    def get_context_data(self, **kwargs):
        context = super(SupplierListView, self).get_context_data(**kwargs)
        supplier_statements = SupplierStatement.objects.all()
        try:
            supplier_amounts = supplier_statements.aggregate(Sum('supplier_amount'))
            supplier_amounts = supplier_amounts.get('supplier_amount__sum')
            payment_amounts = supplier_statements.aggregate(Sum('payment_amount'))
            payment_amounts = payment_amounts.get('payment_amount__sum')
        except:
            supplier_amounts = 0
            payment_amounts = 0

        if supplier_amounts ==None:
            supplier_amounts=0
        if payment_amounts == None:
            payment_amounts = 0

        total_remaining_amount = supplier_amounts - payment_amounts
        context.update({'total_remaining_amount': total_remaining_amount})
        return context

class SupplierStatementListView(ListView):
    model = SupplierStatement
    template_name = "list_supplier_statement.html"
    paginate_by = 40
    ordering='-date'

    def get_queryset(self):
        queryset = SupplierStatement.objects.filter(
            supplier__id=self.kwargs.get('pk')).order_by('-date')  # TODO
        if self.request.GET.get('date'):
            queryset = queryset.filter(
                supplier__name__contains=self.request.GET.get('date'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(SupplierStatementListView,
                        self).get_context_data(**kwargs)
        supplier_statement = SupplierStatement.objects.filter(
            supplier__id=self.kwargs.get('pk'))
        supplier = Supplier.objects.get(id=self.kwargs.get('pk'))
        try:
            supplier_amounts = supplier_statement.aggregate(
                Sum('supplier_amount'))
            supplier_amounts = supplier_amounts.get(
                'supplier_amount__sum') or 0
            payment_amounts = supplier_statement.aggregate(
                Sum('payment_amount'))
            payment_amounts = payment_amounts.get('payment_amount__sum') or 0
        except:
            supplier_amounts = 0
            payment_amounts = 0

        supplier_total_remaining_amount = supplier_amounts - payment_amounts
        context.update({
            'supplier': supplier,
            'supplier_total_remaining_amount': supplier_total_remaining_amount
        })
        return context

class AddSupplierStatementCreateView(CreateView):
    form_class = SupplierStatementForm
    template_name = "add_supplier_statement.html"
    success_url = 'statement_list/<int:pk>'

  
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('login'))
        return super(
            AddSupplierStatementCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save()
        obj.supplier = Supplier.objects.get(
            name=self.request.POST.get('supplier_name'))
        obj.save()
        messages.success(self.request,'Supplier Statement Created!')
        return HttpResponseRedirect(reverse_lazy(
            'list_supplier_statement', kwargs={
                'pk': obj.supplier.id}))

    def form_invalid(self, form):
        messages.error(self.request, 'Error!')
        return super(AddSupplierStatementCreateView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(AddSupplierStatementCreateView,
                        self).get_context_data(**kwargs)
        supplier = (
            Supplier.objects.get(id=self.kwargs.get('pk'))
        )
        context.update({
            'supplier': supplier
        })
        return context

class StatementPaymentCreateView(CreateView):
    form_class = SupplierStatementForm
    template_name = 'statement_payment.html'

   
    def form_valid(self, form):
        obj = form.save()
        messages.success(self.request,'Payment Statement Created!')
        return HttpResponseRedirect(reverse_lazy('list_supplier_statement', kwargs={'pk': self.kwargs.get('pk')}))

    def form_invalid(self, form):
        messages.error(request,'Some Error Occured')
        return super(StatementPaymentCreateView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(StatementPaymentCreateView,
                        self).get_context_data(**kwargs)
        supplier = (
            Supplier.objects.get(id=self.kwargs.get('pk'))
        )
        context.update({
            'supplier': supplier
        })
        return context

class SupplierStatementUpdateView(UpdateView):
    model = SupplierStatement
    template_name = "update_statement.html"
    form_class = SupplierStatementForm

    def form_valid(self, form):
        obj = form.save()
        messages.success(self.request, 'Updated!')
        return HttpResponseRedirect(
            reverse_lazy('list_supplier_statement',
                    kwargs={'pk': obj.supplier.id})
        )

    def form_invalid(self, form):
        return super(SupplierStatementUpdateView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(SupplierStatementUpdateView,
                        self).get_context_data(**kwargs)
        supplier = (
            Supplier.objects.get(supplier__id=self.kwargs.get('pk'))
        )
        context.update({
            'supplier': supplier
        })
        return context


class SupplierDeleteView(DeleteView):
    model = Supplier
    template_name = "list_supplier.html"
    success_url = reverse_lazy('supplier')

    def get(self,request,*args,**kwargs):
        messages.warning(self.request,'Supplier Deleted!')
        return self.delete(request,*args,**kwargs)


class SupplierStatementDeleteView(DeleteView):
    model = SupplierStatement
    template_name = "list_supplier_statement.html"
    def get(self,request,*args,**kwargs):
        self.success_url=request.META['HTTP_REFERER']
        messages.warning(self.request,'Statement Deleted!')
        return self.delete(request,*args,**kwargs)


