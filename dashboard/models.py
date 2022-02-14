from django.db import models


class Bank(models.Model):
    name = models.CharField(max_length=1000, )


class Account(models.Model):
    name = models.CharField(max_length=1000, )
    bank = models.ForeignKey("Bank", on_delete=models.CASCADE)


class Transaction(models.Model):
    name = models.CharField(max_length=1000, )
    amount = models.FloatField()
    date = models.DateField()
    account = models.ForeignKey("Account", on_delete=models.CASCADE)
