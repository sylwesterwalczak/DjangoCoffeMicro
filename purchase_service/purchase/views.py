from django.shortcuts import render
from .models import PurchaseOrder

def change_status(purchase_id, status):
    purchase = PurchaseOrder.objects.get(order_number=purchase_id)
    status_map = {
        'reject': 5,
        'approve': 2
    }
    purchase.status = status_map[status]
    purchase.save()
