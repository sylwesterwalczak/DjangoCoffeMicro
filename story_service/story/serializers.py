import os 
from rest_framework.serializers import ModelSerializer
from authx.utils import  fetch_service_data
from .models import Ingredient


class BaseIngredientSerializer(ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class BaristaIngredientSerializer(BaseIngredientSerializer):
    def to_representation(self, instance):
        api_url = os.environ.get('SUPPLIER_SERVICE')
        ret = super().to_representation(instance)
        ret['supplier'] = fetch_service_data(ret['supplier'], api_url)

        return ret

class ManagerIngredientSerializer(BaseIngredientSerializer):
    def to_representation(self, instance):
        api_url = os.environ.get('SUPPLIER_SERVICE')
        ret = super().to_representation(instance)
        ret['supplier'] = fetch_service_data(ret['supplier'], api_url)

        return ret
