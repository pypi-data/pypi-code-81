# -*- coding: utf-8 -*-
#
# This class was auto-generated from the API references found at
# https://support.direct.ingenico.com/documentation/api/reference/
#
from ingenico.direct.sdk.data_object import DataObject
from ingenico.direct.sdk.domain.amount_of_money import AmountOfMoney
from ingenico.direct.sdk.domain.card_payment_method_specific_output import CardPaymentMethodSpecificOutput
from ingenico.direct.sdk.domain.mobile_payment_method_specific_output import MobilePaymentMethodSpecificOutput
from ingenico.direct.sdk.domain.payment_references import PaymentReferences
from ingenico.direct.sdk.domain.redirect_payment_method_specific_output import RedirectPaymentMethodSpecificOutput
from ingenico.direct.sdk.domain.sepa_direct_debit_payment_method_specific_output import SepaDirectDebitPaymentMethodSpecificOutput


class CaptureOutput(DataObject):
    """
    | Object containing capture details
    """

    __amount_of_money = None
    __amount_paid = None
    __card_payment_method_specific_output = None
    __mobile_payment_method_specific_output = None
    __payment_method = None
    __redirect_payment_method_specific_output = None
    __references = None
    __sepa_direct_debit_payment_method_specific_output = None

    @property
    def amount_of_money(self):
        """
        | Object containing amount and ISO currency code attributes

        Type: :class:`ingenico.direct.sdk.domain.amount_of_money.AmountOfMoney`
        """
        return self.__amount_of_money

    @amount_of_money.setter
    def amount_of_money(self, value):
        self.__amount_of_money = value

    @property
    def amount_paid(self):
        """
        Type: long
        """
        return self.__amount_paid

    @amount_paid.setter
    def amount_paid(self, value):
        self.__amount_paid = value

    @property
    def card_payment_method_specific_output(self):
        """
        | Object containing the card payment method details

        Type: :class:`ingenico.direct.sdk.domain.card_payment_method_specific_output.CardPaymentMethodSpecificOutput`
        """
        return self.__card_payment_method_specific_output

    @card_payment_method_specific_output.setter
    def card_payment_method_specific_output(self, value):
        self.__card_payment_method_specific_output = value

    @property
    def mobile_payment_method_specific_output(self):
        """
        | Object containing the mobile payment method details

        Type: :class:`ingenico.direct.sdk.domain.mobile_payment_method_specific_output.MobilePaymentMethodSpecificOutput`
        """
        return self.__mobile_payment_method_specific_output

    @mobile_payment_method_specific_output.setter
    def mobile_payment_method_specific_output(self, value):
        self.__mobile_payment_method_specific_output = value

    @property
    def payment_method(self):
        """
        | Payment method identifier used by the our payment engine.

        Type: str
        """
        return self.__payment_method

    @payment_method.setter
    def payment_method(self, value):
        self.__payment_method = value

    @property
    def redirect_payment_method_specific_output(self):
        """
        | Object containing the redirect payment product details

        Type: :class:`ingenico.direct.sdk.domain.redirect_payment_method_specific_output.RedirectPaymentMethodSpecificOutput`
        """
        return self.__redirect_payment_method_specific_output

    @redirect_payment_method_specific_output.setter
    def redirect_payment_method_specific_output(self, value):
        self.__redirect_payment_method_specific_output = value

    @property
    def references(self):
        """
        | Object that holds all reference properties that are linked to this transaction

        Type: :class:`ingenico.direct.sdk.domain.payment_references.PaymentReferences`
        """
        return self.__references

    @references.setter
    def references(self, value):
        self.__references = value

    @property
    def sepa_direct_debit_payment_method_specific_output(self):
        """
        | Object containing the SEPA direct debit details

        Type: :class:`ingenico.direct.sdk.domain.sepa_direct_debit_payment_method_specific_output.SepaDirectDebitPaymentMethodSpecificOutput`
        """
        return self.__sepa_direct_debit_payment_method_specific_output

    @sepa_direct_debit_payment_method_specific_output.setter
    def sepa_direct_debit_payment_method_specific_output(self, value):
        self.__sepa_direct_debit_payment_method_specific_output = value

    def to_dictionary(self):
        dictionary = super(CaptureOutput, self).to_dictionary()
        if self.amount_of_money is not None:
            dictionary['amountOfMoney'] = self.amount_of_money.to_dictionary()
        if self.amount_paid is not None:
            dictionary['amountPaid'] = self.amount_paid
        if self.card_payment_method_specific_output is not None:
            dictionary['cardPaymentMethodSpecificOutput'] = self.card_payment_method_specific_output.to_dictionary()
        if self.mobile_payment_method_specific_output is not None:
            dictionary['mobilePaymentMethodSpecificOutput'] = self.mobile_payment_method_specific_output.to_dictionary()
        if self.payment_method is not None:
            dictionary['paymentMethod'] = self.payment_method
        if self.redirect_payment_method_specific_output is not None:
            dictionary['redirectPaymentMethodSpecificOutput'] = self.redirect_payment_method_specific_output.to_dictionary()
        if self.references is not None:
            dictionary['references'] = self.references.to_dictionary()
        if self.sepa_direct_debit_payment_method_specific_output is not None:
            dictionary['sepaDirectDebitPaymentMethodSpecificOutput'] = self.sepa_direct_debit_payment_method_specific_output.to_dictionary()
        return dictionary

    def from_dictionary(self, dictionary):
        super(CaptureOutput, self).from_dictionary(dictionary)
        if 'amountOfMoney' in dictionary:
            if not isinstance(dictionary['amountOfMoney'], dict):
                raise TypeError('value \'{}\' is not a dictionary'.format(dictionary['amountOfMoney']))
            value = AmountOfMoney()
            self.amount_of_money = value.from_dictionary(dictionary['amountOfMoney'])
        if 'amountPaid' in dictionary:
            self.amount_paid = dictionary['amountPaid']
        if 'cardPaymentMethodSpecificOutput' in dictionary:
            if not isinstance(dictionary['cardPaymentMethodSpecificOutput'], dict):
                raise TypeError('value \'{}\' is not a dictionary'.format(dictionary['cardPaymentMethodSpecificOutput']))
            value = CardPaymentMethodSpecificOutput()
            self.card_payment_method_specific_output = value.from_dictionary(dictionary['cardPaymentMethodSpecificOutput'])
        if 'mobilePaymentMethodSpecificOutput' in dictionary:
            if not isinstance(dictionary['mobilePaymentMethodSpecificOutput'], dict):
                raise TypeError('value \'{}\' is not a dictionary'.format(dictionary['mobilePaymentMethodSpecificOutput']))
            value = MobilePaymentMethodSpecificOutput()
            self.mobile_payment_method_specific_output = value.from_dictionary(dictionary['mobilePaymentMethodSpecificOutput'])
        if 'paymentMethod' in dictionary:
            self.payment_method = dictionary['paymentMethod']
        if 'redirectPaymentMethodSpecificOutput' in dictionary:
            if not isinstance(dictionary['redirectPaymentMethodSpecificOutput'], dict):
                raise TypeError('value \'{}\' is not a dictionary'.format(dictionary['redirectPaymentMethodSpecificOutput']))
            value = RedirectPaymentMethodSpecificOutput()
            self.redirect_payment_method_specific_output = value.from_dictionary(dictionary['redirectPaymentMethodSpecificOutput'])
        if 'references' in dictionary:
            if not isinstance(dictionary['references'], dict):
                raise TypeError('value \'{}\' is not a dictionary'.format(dictionary['references']))
            value = PaymentReferences()
            self.references = value.from_dictionary(dictionary['references'])
        if 'sepaDirectDebitPaymentMethodSpecificOutput' in dictionary:
            if not isinstance(dictionary['sepaDirectDebitPaymentMethodSpecificOutput'], dict):
                raise TypeError('value \'{}\' is not a dictionary'.format(dictionary['sepaDirectDebitPaymentMethodSpecificOutput']))
            value = SepaDirectDebitPaymentMethodSpecificOutput()
            self.sepa_direct_debit_payment_method_specific_output = value.from_dictionary(dictionary['sepaDirectDebitPaymentMethodSpecificOutput'])
        return self
