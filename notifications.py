from bittrex.bittrex import Bittrex
from pushbullet import PushBullet
from time import time, sleep
from secret import BITTREX_KEY, BITTREX_SECRET, PUSHBULLET_KEY


PUSHBULLET_API = PUSHBULLET_KEY
LOOP_SLEEP_TIME = 15

pb = PushBullet(api_key=PUSHBULLET_API)
exchange = Bittrex(
    BITTREX_KEY,
    BITTREX_SECRET
)
first_run = True
orders_present = {}

# push = pb.push_note('App started', 'Bittrex notification started')

while True:
    loop_start_time = time()
    orders_to_notify = []

    orders_current = exchange.get_open_orders()['result']

    if first_run:
        for order in orders_current:
            orders_present[order['OrderUuid']] = order
        first_run = False
        continue

    # Build list of uuids present in orders
    order_uuids = [order['OrderUuid'] for order in orders_current]

    # Check if all uuids in orders_present are present in orders
    for uuid in orders_present.keys():
        if uuid in order_uuids:
            continue
        else:
            # Order is gone!
            orders_to_notify.append(orders_present[uuid])

    if len(orders_to_notify) > 0:
        # Push to pushbullet here
        print('Order disappeared! Canceled or sold!')
        note_to_push = ''
        for to_notify in orders_to_notify:
            ex = to_notify['Exchange']
            order_type = to_notify['OrderType']
            limit = to_notify['Limit']
            note_to_push += '%s : %s : %s' % (ex, order_type, limit)
            note_to_push += '\n'
        print(note_to_push)
        pb.push_note('Order moved!', note_to_push)

    # Reset orders_present to the current list
    orders_present = {order['OrderUuid']: order for order in orders_current}
    print('Orders present: %s' % orders_present)

    # Sleep for remaining time
    loop_end_time = time()
    remaining_time = LOOP_SLEEP_TIME - (loop_end_time - loop_start_time)
    sleep(max(0, remaining_time))
