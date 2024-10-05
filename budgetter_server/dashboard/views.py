from concurrent.futures import ThreadPoolExecutor

from django.core.files.uploadedfile import UploadedFile
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from utils.category_predictor import CategoryPredictor, parse_file
from utils.ofxtools import convert_ofx_to_json
from .models import Bank, Account, Category, Transaction
from .serializers import BankSerializer, AccountSerializer, CategorySerializer, TransactionSerializer
from .signals import transactions_created


class BankViewSet(ModelViewSet):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']


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
        transactions_created.send(self.__class__)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    #     training_path = r'D:\Documents\Administratif\Crédit_Agricole\Relevé_comptes\CA20221230_130042_compte_courant.csv'
    #     training_dataset = parse_file(training_path)
    #
    #     predictor = CategoryPredictor(training_dataset, [transaction])


class OFXUploadViewSet(ViewSet):
    """
    A ViewSet for uploading and processing OFX files.
    """

    @action(detail=False, methods=['post'], url_path='upload-ofx')
    def upload_ofx_file(self, request):
        """
        Upload an OFX file to be parsed

        :param request: request sent
        :return: HttpResponse
        """
        if 'file' not in request.FILES:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        file: UploadedFile = request.FILES['file']

        with ThreadPoolExecutor() as executor:
            executor.submit(convert_ofx_to_json, file)

        return Response(status=status.HTTP_200_OK)
