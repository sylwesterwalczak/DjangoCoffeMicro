import os
from datetime import datetime
from authx.utils import fetch_service_data

from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    ListField,
    IntegerField
)
from django.utils.translation import ugettext_lazy as _

from .producer import publish
from .models import PurchaseOrder


class ListPurchaseOrderSerializer(ModelSerializer):
    status = CharField(source='get_status_display')

    class Meta:
        model = PurchaseOrder
        fields = ["status", "order_number"]


class PurchaseOrderSerializer(ModelSerializer):
    def to_representation(self, instance):
        api_url = self.context['api_url']
        ret = super().to_representation(instance)
        new_items = list()

        for item in ret['items']:
            fetched_items = fetch_service_data(
                item, api_url)
            new_items.append(fetched_items)

        ret['items'] = new_items
        return ret

    class Meta:
        model = PurchaseOrder
        fields = '__all__'


class CreatePurchaseOrderSerializer(PurchaseOrderSerializer):
    items = ListField(child=IntegerField())

    def create(self, validated_data):
        purchase = os.environ.get('PURCHASE')
        message_queue = os.environ.get('MESSAGE_QUEUE')

        all_quantity = {}
        api_url = self.context['api_url']

        for item_id in validated_data['items']:
            fetched_items = fetch_service_data(
                item_id, api_url, False)

            for items in fetched_items.get('ingredients'):
                id_number = items.get('id')
                quantity = items.get('quantity')
                if id_number in all_quantity:
                    all_quantity[id_number] += quantity
                else:
                    all_quantity[id_number] = quantity

        body = {
            "items": all_quantity,
            "order_number": validated_data["order_number"]
        }

        publish(
            'created',
            {
                "order_number": validated_data["order_number"],
                "message": "Utworzono zamowienie"
            },
            message_queue
        )
        publish('created', body, purchase)

        return super(CreatePurchaseOrderSerializer, self).create(validated_data)

    def to_internal_value(self, data):
        today = datetime.now()
        conunt_today = PurchaseOrder.objects.filter(
            created_date__date=today).count() + 1
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        data['order_number'] = f"{today.strftime('%d%m%y')}_{conunt_today}"
        data['created_by'] = user.pk

        return super(CreatePurchaseOrderSerializer, self).to_internal_value(data)


class PurchaseOrderSerializerCancelling(ModelSerializer):

    def relese_item(self, data):
        purchase = os.environ.get('PURCHASE')
        message_queue = os.environ.get('MESSAGE_QUEUE')

        all_quantity = {}
        api_url = data["api_url"]

        for item_id in data['items']:
            fetched_items = fetch_service_data(
                item_id, api_url)

            for items in fetched_items.get('ingredients'):
                id_number = items.get('id')
                quantity = items.get('quantity')
                if id_number in all_quantity:
                    all_quantity[id_number] += quantity
                else:
                    all_quantity[id_number] = quantity

        body = {
            "items": all_quantity,
            "order_number": data["order_number"]
        }

        publish('canceled', body, purchase)
        publish(
            'canceled',
            {
                "order_number": data["order_number"],
                "message": "Anulowano zamowienie"
            },
            message_queue
        )

    class Meta:
        model = PurchaseOrder
        fields = "__all__"
