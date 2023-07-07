from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from .models import Bank, Account, Category, Transaction


class BankSerializer(ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'


class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TransactionSerializer(ModelSerializer):

    class Meta:
        model = Transaction
        fields = '__all__'
