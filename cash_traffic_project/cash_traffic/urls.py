from . import views
from django.urls import path

app_name = 'cash_traffic'
urlpatterns = [
     path('', views.ListTransaction.as_view(), name='transactions_list'),
     path('transaction/add', views.add_transaction, name='add_transaction'),
     path('transaction/<int:pk>/edit', views.TransactionUpdateView.as_view(), name='edit_transaction'),
     path('transaction/<int:pk>/delete', views.TransactionDeleteView.as_view(), name='del_transaction'),
     path('status', views.StatusList.as_view(), name='status_list'),
     path('status/add', views.StatusCreateView.as_view(), name='add_status'),
     path('status/<int:pk>/edit', views.StatusUpdateView.as_view(), name='edit_status'),
     path('status/<int:pk>/delete', views.StatusDeleteView.as_view(), name='delete_status'),
     path('type', views.TypeList.as_view(), name='type_list'),
     path('type/add', views.TypeCreateView.as_view(), name='add_type'),
     path('type/<int:pk>/edit', views.TypeUpdateView.as_view(), name='edit_type'),
     path('type/<int:pk>/delete', views.TypeDeleteView.as_view(), name='delete_type'),
     path('category', views.CategoryList.as_view(), name='category_list'),
     path('category/add', views.CategoryCreateView.as_view(), name='add_category'),
     path('category/<int:pk>/edit', views.CategoryUpdateView.as_view(), name='edit_category'),
     path('category/<int:pk>/delete', views.CategoryDeleteView.as_view(), name='delete_category'),
     path('subcategory', views.SubCategoryList.as_view(), name='subcategory_list'),
     path('subcategory/add', views.SubCategoryCreateView.as_view(), name='add_subcategory'),
     path('subcategory/<int:pk>/edit', views.SubCategoryUpdateView.as_view(), name='edit_subcategory'),
     path('subcategory/<int:pk>/delete', views.SubCategoryDeleteView.as_view(), name='delete_subcategory'),
]
