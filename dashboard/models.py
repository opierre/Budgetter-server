from django.db import models


class Bank(models.Model):
    name = models.CharField(max_length=1000, default='')
    logo = models.ImageField(upload_to='uploads/', default=None)


class Account(models.Model):
    name = models.CharField(max_length=1000, default='')
    bank = models.ForeignKey("Bank", on_delete=models.CASCADE)
    amount = models.FloatField(default=0)


class Category(models.Model):
    name = models.CharField(max_length=1000, default='')
    logo = models.ImageField(upload_to='uploads/')


class Transaction(models.Model):

    class Mean(models.TextChoices):
        CARD = 'CARD'
        CASH = 'CASH'
        TRANSFER = 'TR'

    class Type(models.TextChoices):
        EXPENSES = 'EXP'
        INCOME = 'INC'
        TRANSFER = 'TRANSFER'

    name = models.CharField(max_length=1000, default='')
    amount = models.FloatField(default=0)
    date = models.DateField()
    account = models.ForeignKey("Account", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE, null=True, blank=True)
    comment = models.CharField(max_length=4000, default='')
    mean = models.CharField(max_length=1000, choices=Mean.choices, default=Mean.CARD)
    transactionType = models.CharField(max_length=1000, choices=Type.choices, default=Type.EXPENSES)
