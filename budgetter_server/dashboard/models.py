import datetime

from django.utils.translation import gettext as _
from django.db import models


class Mean(models.TextChoices):
    CARD = 'CARD'
    CASH = 'CASH'
    TRANSFER = 'TRANSFER'


class TransactionType(models.TextChoices):
    EXPENSES = 'EXPENSES'
    INCOME = 'INCOME'
    INTERNAL = 'INTERNAL'


class AccountType(models.TextChoices):
    CREDIT_CARD = "CREDIT CARD"


class Status(models.TextChoices):
    ACTIVE = 'ACTIVE'
    CLOSED = 'CLOSED'


class Bank(models.Model):
    name = models.CharField(max_length=1000, default='')
    swift = models.CharField(max_length=1000, default='')
    bic = models.JSONField(default=list)

    def __str__(self):
        return f"{self.name}"


class Account(models.Model):
    name = models.CharField(_("Name"), max_length=1000, default='', null=True, blank=True)
    account_id = models.CharField(_("AccountID"), max_length=1000, default='', unique=True)
    account_type = models.CharField(_("AccountType"), choices=AccountType.choices, default=AccountType.CREDIT_CARD)
    bank = models.ForeignKey("Bank", on_delete=models.CASCADE)
    amount = models.FloatField(_("Amount"), default=0)
    color = models.CharField(_("Color"), max_length=1000, default='')
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
    transaction_type = models.CharField(max_length=1000, choices=TransactionType.choices, default=TransactionType.EXPENSES)
    reference = models.CharField(max_length=1000, default='', unique=True)


class MonthlyCombinedBalance(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    balance = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        unique_together = ('year', 'month')

    def __str__(self):
        return f"{self.year}-{self.month}: {self.balance}"
