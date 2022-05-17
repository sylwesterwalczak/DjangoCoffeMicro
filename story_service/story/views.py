import os
from django.db.models import F

from story.producer import publish
from .models import Ingredient

reply_purchase = os.environ.get('REPLY_PURCHASE')
message_queue = os.environ.get('MESSAGE_QUEUE')


def get_item_quantiy(id):
    all_items = Ingredient.objects.get(id=id)
    return all_items.quantity


def send_message(order_number, message_msg, reply_status):

    publish(
        'created',
        {
            "order_number": order_number,
            "message": message_msg
        },
        message_queue
    )
    publish(
        reply_status,
        {
            "order_number": order_number,
        },
        reply_purchase
    )


def check_story(recived_data, properties):

    is_created = properties.content_type == 'created'
    is_canceled = properties.content_type == 'canceled'

    checked_item = recived_data.get('items')
    
    if is_created:
        for key, item in checked_item.items():
            currrent_qty = get_item_quantiy(key)
            if item > currrent_qty:
                return send_message(recived_data["order_number"], "Odmowa!", "reject")

    obj = list()

    for key, all_res in checked_item.items():
        new_obj = Ingredient.objects.get(pk=key)
        if is_created:
            new_obj.quantity = F('quantity') - all_res
        if is_canceled:
            new_obj.quantity = F('quantity') + all_res

        obj.append(new_obj)

    if is_created:
        return send_message(recived_data["order_number"], "Zamowienie przyjete!!", "approve")
