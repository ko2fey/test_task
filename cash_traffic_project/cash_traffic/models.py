from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone


class Status(models.Model):
    name = models.CharField(max_length=30, unique=True,
                            verbose_name="Название")
    desc = models.CharField(max_length=500, blank=True,
                            null=True, verbose_name="Описание")

    class Meta:
        ordering = ['id']
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

    def __str__(self) -> str:
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=30, unique=True,
                            verbose_name="Название")
    desc = models.CharField(max_length=500, blank=True,
                            null=True, verbose_name="Описание")

    class Meta:
        ordering = ['id']
        verbose_name = 'Тип операции'
        verbose_name_plural = 'Типы операций'

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True,
                            verbose_name="Название")
    type = models.ForeignKey(
        Type, on_delete=models.CASCADE, verbose_name="Тип операции")

    class Meta:
        ordering = ['id']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        unique_together = ('name', 'type')

    def __str__(self) -> str:
        # return f"{self.type}/{self.name}"
        return f"{self.name}"


class SubCategory(models.Model):
    name = models.CharField(max_length=30, unique=True,
                            verbose_name="Название подкатегории")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="Категория")

    class Meta:
        ordering = ['id']
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
        unique_together = ('name', 'category')

    def __str__(self) -> str:
        # return f"{self.category.name}/{self.name}"
        return f"{self.name}"


class Transaction(models.Model):
    date_created = models.DateTimeField(auto_now=True, verbose_name="Дата создания")
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name="Статус"
    )
    type = models.ForeignKey(
        Type,
        on_delete=models.PROTECT,
        verbose_name="Тип операции"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name="Категория"
    )
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.PROTECT,
        verbose_name="Подкатегория"
    )
    amount = models.DecimalField(
        max_digits=11,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name="Сумма"
    )
    comment = models.TextField(
        blank=True,
        null=True,
        verbose_name="Комментарий"
    )

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'
        ordering = ['-date_created']

    # def save(self, *args, **kwargs):
    #     if self.category != self.subcategory.category:
    #         raise ValueError(
    #             "Выбранная подкатегория не принадлежит данной категории.")
    #     if self.type != self.category.type:
    #         raise ValueError(
    #             "Выбранная категория не принадлежит данному типу операций.")
    #     super().save(*args, **kwargs)

    def __str__(self) -> str:
        data_created = timezone.datetime.strftime(
            self.date_created, "%m-%d-%Y %H:%M:%S")
        return f"{data_created} - {self.amount} - {self.comment}"
