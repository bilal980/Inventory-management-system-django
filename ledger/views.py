from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist
from customer.forms import CustomerForm
from ledger.models import Ledger
from ledger.forms import LedgerForm
from django.views.generic import FormView, DeleteView
from customer.models import Customer
from django.core.paginator import Paginator


class AddNewLedger(FormView):
    form_class = CustomerForm
    template_name = 'create_ledger.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super(AddNewLedger, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        customer = form.save()
        ledger_form_kwargs = {
            'customer': customer.id,
            'person': self.request.POST.get('customer_type'),
            'amount': self.request.POST.get('amount'),
            'payment_amount': self.request.POST.get('payment_amount'),
            'payment_type': self.request.POST.get('payment_type'),
            'description': self.request.POST.get('description'),
        }

        ledger_form = LedgerForm(ledger_form_kwargs)
        if ledger_form.is_valid():
            ledger_form.save()

        messages.success(self.request, 'Ledger Created')
        return HttpResponseRedirect(reverse('customer_ledger_list'))

    def form_invalid(self, form):
        messages.error(self.request, 'Some Error Occured')
        return super(AddNewLedger, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(AddNewLedger, self).get_context_data(**kwargs)
        customers = Customer.objects.all()

        context.update({
            'customers': customers
        })

        return context


def customer_ledger_view(request):
    customers = (Customer.objects.all().order_by('customer_name'))
    customer_ledger = []
    for customer in customers:
        customer_data = {}
        ledger = customer.customer_ledger.all().aggregate(Sum('amount'))
        payment_ledger = customer.customer_ledger.all().aggregate(Sum('payment'))

        if payment_ledger.get('payment__sum'):
            payment_amount = float(payment_ledger.get('payment__sum'))
        else:
            payment_amount = 0

        if ledger.get('amount__sum'):
            ledger_amount = float(ledger.get('amount__sum'))
        else:
            ledger_amount = 0

        remaining_ledger = '%g' % (ledger_amount - payment_amount)
        customer_data.update({
            'id': customer.id,
            'ledger_amount': ledger_amount,
            'payment_amount': payment_amount,
            'customer_name': customer.customer_name,
            'customer_phone': customer.customer_phone,
            'remaining_ledger': remaining_ledger,
            'customer_type': customer.customer_type,
        })
        customer_ledger.append(customer_data)

    ledgers = Ledger.objects.all()
    if ledgers:
        grand_ledger = ledgers.aggregate(Sum('amount'))
        grand_ledger = float(grand_ledger.get('amount__sum') or 0)

        grand_payment = ledgers.aggregate(Sum('payment'))
        grand_payment = float(grand_payment.get('payment__sum') or 0)

        total_remaining_amount = grand_ledger - grand_payment

    else:
        total_remaining_amount = 0

    paginator = Paginator(customer_ledger, 15)
    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)
    return render(request, 'customer_ledger_list.html', {'customer_ledgers': page_obj,  'total_remaining_amount': total_remaining_amount, })

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super(
            CustomerLedgerDetailsView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(
            CustomerLedgerDetailsView, self).get_context_data(**kwargs)

        try:
            customer = Customer.objects.get(id=self.kwargs.get('pk')
                                            )
        except Customer.DoesNotExist:
            raise Http404

        ledgers = customer.customer_ledger.all()
        if ledgers:
            ledger_total = ledgers.aggregate(Sum('amount'))
            ledger_total = float(ledger_total.get('amount__sum'))
            context.update({

            })
        else:
            ledger_total = 0

        if ledgers:
            payment_total = ledgers.aggregate(Sum('payment'))
            payment_total = float(payment_total.get('payment__sum'))
            context.update({

            })
        else:
            payment_total = 0

        context.update({
            'customer': customer,
            'ledgers': ledgers.order_by('-dated'),
            'ledger_total': '%g' % ledger_total,
            'payment_total': '%g' % payment_total,
            'remaining_amount': '%g' % (ledger_total - payment_total)
        })

        return context


def customer_ledger_detail_list(request, pk):
    context = {}
    try:
        customer = Customer.objects.get(id=pk)
    except Customer.DoesNotExist:
        raise Http404
    ledgers = customer.customer_ledger.all()
    if ledgers:
        ledger_total = ledgers.aggregate(Sum('amount'))
        ledger_total = float(ledger_total.get('amount__sum'))
        context.update({
        })
    else:
        ledger_total = 0
    if ledgers:
        payment_total = ledgers.aggregate(Sum('payment'))
        payment_total = float(payment_total.get('payment__sum'))
        context.update({

        })
    else:
        payment_total = 0

    ledgers = ledgers.order_by('-dated')
    paginator = Paginator(ledgers, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context.update({
        'customer': customer,
        'ledgers': page_obj,
        'ledger_total': '%g' % ledger_total,
        'payment_total': '%g' % payment_total,
        'remaining_amount': '%g' % (ledger_total - payment_total)
    })

    return render(request, 'customer_ledger_details.html', context)


class AddLedger(FormView):
    template_name = 'add_customer_ledger.html'
    form_class = LedgerForm

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super(AddLedger, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        ledger = form.save()
        messages.success(self.request, 'Ledger Created!')
        return HttpResponseRedirect(reverse('customer_ledger_detail', kwargs={'pk': self.kwargs.get('pk')})
                                    )

    def form_invalid(self, form):
        messages.error(self.request, 'Some Error Occured')

        return super(AddLedger, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(AddLedger, self).get_context_data(**kwargs)
        try:
            customer = (
                Customer.objects.get(id=self.kwargs.get('pk'))
            )
        except ObjectDoesNotExist:
            raise Http404('Customer not found with concerned User')

        context.update({
            'customer': customer
        })
        return context


class AddPayment(FormView):
    template_name = 'add_payment.html'
    form_class = LedgerForm

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super(AddPayment, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        ledger = form.save()
        messages.success(self.request, 'Payment Added!')
        return HttpResponseRedirect(
            reverse('customer_ledger_detail', kwargs={'pk': self.kwargs.get('pk')
                                                      })
        )

    def form_invalid(self, form):
        messages.warning(self.request, 'Error!')
        return super(AddPayment, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(AddPayment, self).get_context_data(**kwargs)
        try:
            customer = (
                Customer.objects.get(id=self.kwargs.get('pk'))
            )
        except ObjectDoesNotExist:
            raise Http404('Customer not found with concerned User')

        context.update({
            'customer': customer
        })
        return context


class LedgerDeleteView(DeleteView):
    model = Ledger
    template_name = "customer_ledger_list.html"

    def get(self, request, *args, **kwargs):
        self.success_url = request.META['HTTP_REFERER']
        # print(customer.customer_name)
        # print('done')
        messages.warning(request, 'Ledger Deleted !')
        print('again done')
        return self.delete(request,*args,**kwargs)


class CustomerLedgerDeleteView(DeleteView):
    model = Ledger
    template_name = "customer_ledger_list.html"

    def get(self,request,*args,**kwargs):
        # self.success_url = request.META['HTTP_REFERER']
        customer = Customer.objects.get(id=self.kwargs.get('pk'))
        Ledger.objects.filter(customer=customer).delete()
        messages.warning(request,f'{customer.customer_name} Ledger Deleted!')
        return redirect(request.META['HTTP_REFERER'])
