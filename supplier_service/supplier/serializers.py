from rest_framework.serializers import ModelSerializer, ReadOnlyField
from .models import Supplier


class SupplierSerializer(ModelSerializer):
    custom_id = ReadOnlyField()

    class Meta:
        model = Supplier
        fields = ['custom_id']


class AdminSupplierSerializer(SupplierSerializer):

    class Meta:
        model = Supplier
        fields = '__all__'
