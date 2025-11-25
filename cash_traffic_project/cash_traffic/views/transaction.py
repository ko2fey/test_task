from ..forms import FormTransaction
from ..models import Transaction
from ..filter import TransactionFilter
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy

# Для примера сделал 1 представление (add_transaction) через функцию а не Класс 

class ListTransaction(ListView):
    model = Transaction
    template_name = 'cash_traffic/index.html'
    context_object_name = 'transactions'
    paginate_by = 5
    
    def get_queryset(self):
        queryset = super().get_queryset() # type: ignore
        self.filter = TransactionFilter(self.request.GET, queryset=queryset) # type: ignore
        return self.filter.qs
    
    def get_context_data(self, **kwargs):  
        url_param = self.request.GET.copy()
        if 'page' in url_param:
            del url_param['page']
        
        context = super().get_context_data(**kwargs) # type: ignore
        context['title'] = 'Список транзакций'
        context['header'] = 'Доска'
        context['filter'] = self.filter
        context['filter_params'] = url_param.urlencode() # type: ignore
        return context
    
def add_transaction(request):
    if request.method == 'POST':
        form = FormTransaction(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('cash_traffic:transactions_list')
            except Exception as e:
                form.add_error(None, f'Произошла ошибка при сохранении транзакции. {e}')
    else:
        form = FormTransaction()
    return render(request, 'cash_traffic/add_transaction.html', {'form': form, 'header': 'Добавить транзакцию'})

class TransactionUpdateView(UpdateView):
    model = Transaction
    form_class = FormTransaction 
    template_name = 'cash_traffic/add_transaction.html'
    success_url = reverse_lazy('cash_traffic:transactions_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Редактировать транзакцию'
        return context

class TransactionDeleteView(DeleteView):
    model = Transaction
    template_name = 'cash_traffic/confirm_del.html'
    success_url = reverse_lazy('cash_traffic:transactions_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Удалить транзакцию'
        context['cancel_url'] = reverse_lazy('cash_traffic:transactions_list')
        return context