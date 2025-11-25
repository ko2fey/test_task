from django.forms import ModelForm, ModelChoiceField
from django_select2.forms import ModelSelect2Widget
from .models import Transaction, Status, Category, SubCategory, Type
from django.core.exceptions import ValidationError

class FormTransaction(ModelForm):
    status = ModelChoiceField(
        queryset=Status.objects.all(),
        widget=ModelSelect2Widget(
            model=Type,
            search_fields=['name__icontains'],
            attrs={
                'data-placeholder': 'Выберите статус',
                'data-minimum-input-length': 0,
                'theme': 'bootstrap-5',
                'class': 'form-select',
            },
            
        )
    )
    
    type = ModelChoiceField(
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
            
        )
    )
    
    category = ModelChoiceField(
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
    
    subcategory = ModelChoiceField(
        queryset=SubCategory.objects.all(),
        widget=ModelSelect2Widget(
            model=SubCategory,
            search_fields=['name__icontains'],
            dependent_fields={
                'category': 'category',
            },            
            attrs={
                'data-placeholder': 'Выберите подкатегорию',
                'data-minimum-input-length': 0,
                'data-theme': 'bootstrap-5',
                'class': 'form-select',
            }
        )
    )
    
    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        subcategory = cleaned_data.get('subcategory') 
        type_op = cleaned_data.get('type')
        
        errors = {}
        
        if category and subcategory and category != subcategory.category:
            errors['subcategory'] = "Подкатегория не принадлежит выбранной категории"
        
        if category and type_op and category.type != type_op:
            errors['type'] = "Категория не принадлежит выбранному типу операции"
        
        if errors:
            raise ValidationError(errors)
        
        return cleaned_data
    class Meta:
        model = Transaction
        fields = '__all__'

class FormType(ModelForm):
    class Meta:
        model = Type
        fields = '__all__'

class FormStatus(ModelForm):
    class Meta:
        model = Status
        fields = '__all__'


class FormCategory(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class FormSubCategory(ModelForm):
    class Meta:
        model = SubCategory
        fields = '__all__'
