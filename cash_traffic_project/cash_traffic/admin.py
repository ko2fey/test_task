from django.contrib import admin
from .models import Transaction, Status, Category, SubCategory, Type

# Подключаем модели для возможности работы с ними в админке
# Небольшие косметические настройки для вывода транзакций + фильтрация
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['date_created', 'status', 'type', 'category', 'subcategory', 'amount', 'comment']
    list_filter = ['status', 'type', 'category', 'subcategory', 'date_created']
    search_fields = ['comment', 'amount']
    date_hierarchy = 'date_created'
admin.site.register(Status)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Type)
