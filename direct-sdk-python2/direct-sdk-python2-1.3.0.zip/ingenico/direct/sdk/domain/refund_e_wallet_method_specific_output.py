# -*- coding: utf-8 -*-
#
# This class was auto-generated from the API references found at
# https://support.direct.ingenico.com/documentation/api/reference/
#
from ingenico.direct.sdk.data_object import DataObject
from ingenico.direct.sdk.domain.refund_payment_product840_specific_output import RefundPaymentProduct840SpecificOutput


class RefundEWalletMethodSpecificOutput(DataObject):

    __payment_product840_specific_output = None
    __total_amount_paid = None
    __total_amount_refunded = None

    @property
    def payment_product840_specific_output(self):
        """
        Type: :class:`ingenico.direct.sdk.domain.refund_payment_product840_specific_output.RefundPaymentProduct840SpecificOutput`
        """
        return self.__payment_product840_specific_output

    @payment_product840_specific_output.setter
    def payment_product840_specific_output(self, value):
        self.__payment_product840_specific_output = value

    @property
    def total_amount_paid(self):
        """
        Type: long
        """
        return self.__total_amount_paid

    @total_amount_paid.setter
    def total_amount_paid(self, value):
        self.__total_amount_paid = value

    @property
    def total_amount_refunded(self):
        """
        Type: long
        """
        return self.__total_amount_refunded

    @total_amount_refunded.setter
    def total_amount_refunded(self, value):
        self.__total_amount_refunded = value

    def to_dictionary(self):
        dictionary = super(RefundEWalletMethodSpecificOutput, self).to_dictionary()
        if self.payment_product840_specific_output is not None:
            dictionary['paymentProduct840SpecificOutput'] = self.payment_product840_specific_output.to_dictionary()
        if self.total_amount_paid is not None:
            dictionary['totalAmountPaid'] = self.total_amount_paid
        if self.total_amount_refunded is not None:
            dictionary['totalAmountRefunded'] = self.total_amount_refunded
        return dictionary

    def from_dictionary(self, dictionary):
        super(RefundEWalletMethodSpecificOutput, self).from_dictionary(dictionary)
        if 'paymentProduct840SpecificOutput' in dictionary:
            if not isinstance(dictionary['paymentProduct840SpecificOutput'], dict):
                raise TypeError('value \'{}\' is not a dictionary'.format(dictionary['paymentProduct840SpecificOutput']))
            value = RefundPaymentProduct840SpecificOutput()
            self.payment_product840_specific_output = value.from_dictionary(dictionary['paymentProduct840SpecificOutput'])
        if 'totalAmountPaid' in dictionary:
            self.total_amount_paid = dictionary['totalAmountPaid']
        if 'totalAmountRefunded' in dictionary:
            self.total_amount_refunded = dictionary['totalAmountRefunded']
        return self
