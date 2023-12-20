import datetime

from django.utils.translation import gettext as _
from django.db import models


class Mean(models.TextChoices):
    CARD = 'CARD'
    CASH = 'CASH'
    TRANSFER = 'TRANSFER'


class Type(models.TextChoices):
    EXPENSES = 'EXPENSES'
    INCOME = 'INCOME'
    INTERNAL = 'INTERNAL'


class Status(models.TextChoices):
    ACTIVE = 'ACTIVE'
    CLOSED = 'CLOSED'


class ExpensesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(transaction_type='EXPENSES')


class IncomeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(transactionType='INCOME')


class Bank(models.Model):
    name = models.CharField(max_length=1000, default='')
    swift = models.CharField(max_length=1000, default='')
    bic = models.JSONField(default=list)

    def __str__(self):
        return f"{self.name}"


class Account(models.Model):
    name = models.CharField(_("Name"), max_length=1000, default='')
    account_id = models.CharField(_("AccountID"), max_length=1000, default='')
    bank = models.ForeignKey("Bank", on_delete=models.CASCADE)
    amount = models.FloatField(_("Amount"), default=0)
    color = models.CharField(_("Color"), max_length=1000, default='#ffffff')
    last_update = models.DateField(_("Date"), default=datetime.date.today)
    status = models.CharField(_("State"), choices=Status.choices, default=Status.ACTIVE)


class Category(models.Model):
    name = models.CharField(max_length=1000, default='')


class Transaction(models.Model):
    name = models.CharField(max_length=1000, default='')
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    date = models.DateField()
    account = models.ForeignKey("Account", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE, null=True, blank=True)
    comment = models.CharField(max_length=4000, default='', blank=True)
    mean = models.CharField(max_length=1000, choices=Mean.choices, default=Mean.CARD)
    transaction_type = models.CharField(max_length=1000, choices=Type.choices, default=Type.EXPENSES)

    # Define managers
    objects = models.Manager()
    expenses = ExpensesManager()
    income = IncomeManager()
