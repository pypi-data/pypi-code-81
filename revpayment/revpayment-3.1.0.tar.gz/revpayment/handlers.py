from revpayment.settings import api_settings


class BaseHandler:
    tracking_fields = {"payment_status": "payment"}

    def __init__(self, order):
        self.order = order

    def get_state_meta(self, state):
        from revpayment.carts import Cart

        buyer = api_settings.BUYER_CLASS.objects.get(id=state.buyer_id)
        cart = Cart(buyer)
        return cart, buyer

    def on_payment_result(self, changed):
        created = changed.get("__created", False)
        if created:
            self.on_order_create()
        for k, v in changed.items():
            if k in self.tracking_fields:
                previous = changed.get(f"_{k}", None)
                func = getattr(self, f"on_{self.tracking_fields[k]}_{v}", None)
                if func:
                    func(previous)

    def before_checkout(
        self, cart, order_id, order_type, payment_type, payment_subtype
    ):
        raise NotImplementedError

    def after_checkout(self, cart, order_id, order_type, payment_type, payment_subtype):
        raise NotImplementedError

    def on_order_create(self):
        raise NotImplementedError


class Handler(BaseHandler):
    def on_payment_success(self, previous):
        if self.order.order_type == "credit":
            buyer = self.order.buyer
            buyer.payment.credit += self.order.amount
            buyer.payment.save()

    def on_payment_failure(self, previous):
        return

    def before_checkout(self, *args, **kwargs):
        return

    def after_checkout(self, *args, **kwargs):
        return

    def on_order_create(self):
        return
