# Разбиливаем представления на модули
# Используем старндартные классы Django 
# Используем ListView, UpdateView, DeleteView, CreateView для создания представлений
from .status import *
from .transaction import *
from .type import *
from .category import *
from .subcategory import *
from .mixins import *