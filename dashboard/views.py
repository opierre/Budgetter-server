from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from budgetter.settings import BASE_DIR
from dashboard.models import *
from dashboard.serializers import *


class BankViewSet(ModelViewSet):
    queryset = Bank.objects.all()
    serializer = BankSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']


class AccountViewSet(ModelViewSet):
    queryset = Account.objects.all()
    serializer = AccountSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'bank']


class CategoryViewSet(ModelViewSet):
    queryset = Account.objects.all()
    serializer = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']


class TransactionViewSet(ModelViewSet):
    queryset = Account.objects.all()
    serializer = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'amount', 'date']




