import django_filters
from django import forms
from django_select2.forms import ModelSelect2Widget
from .models import Transaction, Type, Category

# Создаем фильтр для списка транзакций который будет нужен нам в нашей вьюхе
class DateInput(forms.DateInput):
    input_type = 'date'
    
class TransactionFilter(django_filters.FilterSet):
    amount_min = django_filters.NumberFilter(field_name='amount', lookup_expr='gte')
    amount_max = django_filters.NumberFilter(field_name='amount', lookup_expr='lte')
    date_after = django_filters.DateFilter(field_name='date_created', lookup_expr='gte', widget=DateInput)
    date_before = django_filters.DateFilter(field_name='date', lookup_expr='lte', widget=DateInput)
    type = django_filters.ModelChoiceFilter(
        field_name='type', 
        queryset=Type.objects.all(), 
        widget=ModelSelect2Widget(
            model=Type,
            search_fields=['name__icontains'],
            attrs={
                'data-placeholder': 'Выберите тип операции',
                'data-minimum-input-length': 0,
                'data-width': '100%',
                'theme': 'bootstrap-5',
                'class': 'form-select',
            },
        ))
    category = django_filters.ModelChoiceFilter(
        field_name='category',
        queryset=Category.objects.all(),
        widget=ModelSelect2Widget(
            model=Category,
            search_fields=['name__icontains'],
            dependent_fields={'type': 'type'},            
            attrs={
                'data-placeholder': 'Выберите категорию',
                'data-minimum-input-length': 0,
                'data-theme': 'bootstrap-5',
                'class': 'form-select',
            }
        )
    )
    
    # Сортировка
    ordering = django_filters.OrderingFilter(
        choices=(
            ('date_created', 'По дате (возрастания)'),
            ('-date_created', 'По дате (убывания)'),
            ('amount', 'По сумме (возрастания)'),
            ('-amount', 'По сумме (убывания)'),
        ),
        fields={
            'date_created': 'date_created',
            'amount': 'amount',
        }
    )
    
    class Meta:
        model = Transaction
        fields = ['category']