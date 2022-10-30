from django.db import models


class Mean(models.TextChoices):
    CARD = 'CARD'
    CASH = 'CASH'
    TRANSFER = 'TR'


class Type(models.TextChoices):
    EXPENSES = 'EXPENSES'
    INCOME = 'INCOME'
    TRANSFER = 'TRANSFER'


class ExpensesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(transaction_type='EXPENSES')


class IncomeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(transactionType='INCOME')


class Bank(models.Model):
    name = models.CharField(max_length=1000, default='')

    def __str__(self):
        return f"{self.name}"


class Account(models.Model):
    name = models.CharField(max_length=1000, default='')
    bank = models.ForeignKey("Bank", on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    color = models.CharField(max_length=1000, default='#ffffff')


class Category(models.Model):
    name = models.CharField(max_length=1000, default='')
    logo = models.ImageField(upload_to='uploads/')


class Transaction(models.Model):
    name = models.CharField(max_length=1000, default='')
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    date = models.DateField()
    account = models.ForeignKey("Account", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE, null=True, blank=True)
    comment = models.CharField(max_length=4000, default='')
    mean = models.CharField(max_length=1000, choices=Mean.choices, default=Mean.CARD)
    transaction_type = models.CharField(max_length=1000, choices=Type.choices, default=Type.EXPENSES)

    # Define managers
    objects = models.Manager()
    expenses = ExpensesManager()
    income = IncomeManager()
