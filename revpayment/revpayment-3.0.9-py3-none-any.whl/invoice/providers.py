import copy

from revpayment import actions
from revpayment.invoice import actions as invoice_actions


class BaseInvoiceMeta(type):
    def __new__(cls, names, bases, attrs):
        attrs["_declared_actions"] = {}
        for v in bases:
            _declared = getattr(v, "_declared_actions", {})
            declared = copy.deepcopy(_declared)
            attrs["_declared_actions"] = {**declared, **attrs["_declared_actions"]}

        for k, v in attrs.items():
            if isinstance(v, type) and issubclass(v, actions.BaseAction):
                attrs["_declared_actions"][k] = v
        return super().__new__(cls, names, bases, attrs)


class BaseProvider(metaclass=BaseInvoiceMeta):
    def __init__(self, *args, **kwargs):
        for k, v in self.__class__._declared_actions.items():
            use_action = getattr(self, f"use_{k}", None)
            action = v(*args, **kwargs)
            if use_action and callable(use_action):
                setattr(self, f"_{k}", action.perform)
                setattr(self, k, use_action)
            else:
                setattr(self, k, action.perform)


class EcpayProvider(BaseProvider):
    issue_invoice = invoice_actions.EcpayIssue


class NewebProvider(BaseProvider):
    issue_invoice = invoice_actions.NewebIssue
