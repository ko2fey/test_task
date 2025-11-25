from ..forms import FormCategory
from ..models import Category
from django.shortcuts import redirect
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.db.models import ProtectedError
from django.contrib import messages

class CategoryList(ListView):
    model = Category
    template_name = 'cash_traffic/Category_list.html'
    context_object_name = 'сategoryes'
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        context['header'] = 'Список категорий'
        return context

class CategoryCreateView(CreateView):
    model = Category
    form_class = FormCategory
    template_name = 'cash_traffic/add_category.html'
    success_url = reverse_lazy('cash_traffic:category_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Добавить категорию'
        return context

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = FormCategory
    template_name = 'cash_traffic/add_category.html'
    success_url = reverse_lazy('cash_traffic:category_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Редактировать категорию'
        return context

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'cash_traffic/confirm_del.html'
    success_url = reverse_lazy('cash_traffic:category_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Удалить категорию'
        context['cancel_url'] = reverse_lazy('cash_traffic:category_list')
        return context
    
    def form_valid(self, form):
        try:
            return super().form_valid(form) # type: ignore
        except ProtectedError as e:
            self.object = self.get_object()
            protected_objects = list(e.protected_objects)
            messages.error(
                self.request, 
                f'Нельзя удалить категорию "{self.object}", так как она используется в {len(protected_objects)} транзакциях'
            )
        except Exception as e:
            messages.error(self.request, f'Ошибка при удалении: {str(e)}')
        return redirect('cash_traffic:category_list')