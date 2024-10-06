import os.path
from typing import Union

from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from budgetter.settings import MEDIA_ROOT
from .models import Bank, Account, Category, Transaction


class BankSerializer(ModelSerializer):
    svg_content = SerializerMethodField(read_only=True)

    class Meta:
        model = Bank
        fields = '__all__'

    @staticmethod
    def get_svg_content(bank_obj: Bank) -> Union[str, None]:
        """
        Return SVG content from logo

        :param bank_obj: bank instance
        :return: SVG content as string
        """

        try:
            bank_logo = os.path.join(MEDIA_ROOT, "logo", f"{bank_obj.name.lower().replace(' ', '_')}.svg")
            with open(bank_logo, 'r') as svg_file:
                svg_data = svg_file.read()
            return svg_data
        except FileNotFoundError:
            return None


class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TransactionSerializer(ModelSerializer):
    date = serializers.DateField(format="%Y-%m-%d", required=False)  # ISO 8601 format

    class Meta:
        model = Transaction
        fields = '__all__'
