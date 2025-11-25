from ..forms import FormStatus
from ..models import Status
from django.shortcuts import redirect
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.db.models import ProtectedError
from django.contrib import messages

class StatusList(ListView):
    model = Status
    template_name = 'cash_traffic/status_list.html'
    context_object_name = 'statuses'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Список статусов'
        return context

class StatusCreateView(CreateView):
    model = Status
    form_class = FormStatus
    template_name = 'cash_traffic/add_status.html'
    success_url = reverse_lazy('cash_traffic:status_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Добавить статус'
        return context

class StatusUpdateView(UpdateView):
    model = Status
    form_class = FormStatus
    template_name = 'cash_traffic/add_status.html'
    success_url = reverse_lazy('cash_traffic:status_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Редактировать статус'
        return context

class StatusDeleteView(DeleteView):
    model = Status
    template_name = 'cash_traffic/confirm_del.html'
    success_url = reverse_lazy('cash_traffic:status_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Удалить статус'
        context['cancel_url'] = reverse_lazy('cash_traffic:status_list')
        return context
    
    def form_valid(self, form):
        try:
            return super().form_valid(form) # type: ignore
        except ProtectedError as e:
            self.object = self.get_object()
            protected_objects = list(e.protected_objects)
            messages.error(
                self.request, 
                f'Нельзя удалить статус "{self.object}", так как он используется в {len(protected_objects)} транзакциях'
            )
        except Exception as e:
            messages.error(self.request, f'Ошибка при удалении: {str(e)}')
        return redirect('cash_traffic:status_list')