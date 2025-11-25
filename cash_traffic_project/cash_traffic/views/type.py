from ..forms import FormType
from ..models import Type
from django.shortcuts import redirect
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.db.models import ProtectedError
from django.contrib import messages

class TypeList(ListView):
    model = Type
    template_name = 'cash_traffic/type_list.html'
    context_object_name = 'types'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Список типов'
        return context

class TypeCreateView(CreateView):
    model = Type
    form_class = FormType
    template_name = 'cash_traffic/add_type.html'
    success_url = reverse_lazy('cash_traffic:type_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Добавить тип'
        return context

class TypeUpdateView(UpdateView):
    model = Type
    form_class = FormType
    template_name = 'cash_traffic/add_type.html'
    success_url = reverse_lazy('cash_traffic:type_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Редактировать тип'
        return context

class TypeDeleteView(DeleteView):
    model = Type
    template_name = 'cash_traffic/confirm_del.html'
    success_url = reverse_lazy('cash_traffic:type_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Удалить тип'
        context['cancel_url'] = reverse_lazy('cash_traffic:type_list')
        return context
    
    def form_valid(self, form):
        try:
            return super().form_valid(form) # type: ignore
        except ProtectedError as e:
            self.object = self.get_object()
            protected_objects = list(e.protected_objects)
            messages.error(
                self.request, 
                f'Нельзя удалить тип "{self.object}", так как он используется в {len(protected_objects)} транзакциях'
            )
        except Exception as e:
            messages.error(self.request, f'Ошибка при удалении: {str(e)}')
        return redirect('cash_traffic:Type_list')