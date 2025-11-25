from ..forms import FormSubCategory
from ..models import SubCategory
from django.shortcuts import redirect
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.db.models import ProtectedError
from django.contrib import messages

class SubCategoryList(ListView):
    model = SubCategory
    template_name = 'cash_traffic/subcategory_list.html'
    context_object_name = 'subcategoryes'
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        context['header'] = 'Список подкатегорий'
        return context

class SubCategoryCreateView(CreateView):
    model = SubCategory
    form_class = FormSubCategory
    template_name = 'cash_traffic/add_subcategory.html'
    success_url = reverse_lazy('cash_traffic:subcategory_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Добавить подкатегорию'
        return context

class SubCategoryUpdateView(UpdateView):
    model = SubCategory
    form_class = FormSubCategory
    template_name = 'cash_traffic/add_subcategory.html'
    success_url = reverse_lazy('cash_traffic:subcategory_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Редактировать подкатегорию'
        return context

class SubCategoryDeleteView(DeleteView):
    model = SubCategory
    template_name = 'cash_traffic/confirm_del.html'
    success_url = reverse_lazy('cash_traffic:subcategory_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Удалить подкатегорию'
        context['cancel_url'] = reverse_lazy('cash_traffic:subcategory_list')
        return context
    
    def form_valid(self, form):
        try:
            return super().form_valid(form) # type: ignore
        except ProtectedError as e:
            self.object = self.get_object()
            protected_objects = list(e.protected_objects)
            messages.error(
                self.request, 
                f'Нельзя удалить подкатегорию "{self.object}", так как она используется в {len(protected_objects)} транзакциях'
            )
        except Exception as e:
            messages.error(self.request, f'Ошибка при удалении: {str(e)}')
        return redirect('cash_traffic:Subcategory_list')