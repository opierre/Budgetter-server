from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from utils.category_predictor import CategoryPredictor, parse_file
from .models import Bank, Account, Category, Transaction
from .serializers import BankSerializer, AccountSerializer, CategorySerializer, TransactionSerializer


class BankViewSet(ModelViewSet):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']

    # def list(self, request, *args, **kwargs):
    #     """
    #     Override list method to include SVG content for logo
    #
    #     :param request: request
    #     :param args: args
    #     :param kwargs: kwargs
    #     :return: Response
    #     """
    #
    #     serializer = self.get_serializer(data=request.data, many=True)
    #     serializer.is_valid(raise_exception=True)




class AccountViewSet(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'bank']


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']


class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'amount', 'date']

    def create(self, request, *args, **kwargs):
        """
        Override create to find matching category first and multiple objects

        :param request: request
        :param args: args
        :param kwargs: kwargs
        :return: Response
        """

        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    #     training_path = r'D:\Documents\Administratif\Crédit_Agricole\Relevé_comptes\CA20221230_130042_compte_courant.csv'
    #     training_dataset = parse_file(training_path)
    #
    #     predictor = CategoryPredictor(training_dataset, [transaction])


