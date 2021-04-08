class SubscriptionRequestFromPartnerForm:
    """Mapping class to convert the PartnerForm of Tryton in a
               SubscriptionRequest dict expected in the API.

            * Partner data dict:

    ```
            {
              "partner_do_option": "do_partner",
              "partner_number": "",
              "name": "Lisa",
              "lastname": "Johnson",
              "surname": "Stevenson",
              "tradename": "",
              "lang": "ca",
              "birth_date": "1993-6-26",
              "vat_number": "21196232F",
              "email": "huertageorge@morris-sandoval.info",
              "phone": "666 666 666",
              "sex": "male",
              "bank_iban": "ES6621000418401234567891",
              "street": "Graner 10",
              "zip": "08904",
              "city": "LH",
              "party_type": "person",
              "password": "12345678",

              # To transform to models
              "nationality": "64",
              "subdivision": "4487",
              "country": "64",

              # To investigate
              "contribute_somconnexio_option": "0",

              # API como las telecom_companies
              "discovery_channel": "1",

              # Unused
              "invoice_name": ""
              "invoice_lastname": "",
              "invoice_phone": "",
              "invoice_street": "",
              "invoice_country": "64",
              "invoice_zip": "",
              "invoice_city": "",
              "invoice_surname": "",
              "galatea_website": 4,
            }
    ```

            * SubscriptionRequest:

            Attributes:
                partner_form: PartnerForm from SomConnexio Tryton Galatea module
    """

    def __init__(self, partner_data):
        self.partner_data = partner_data

    def to_dict(self):
        name = self._get_name()
        sr_dict = {
            "type": self._type(),
            "name": name,
            "firstname": self.partner_data.get("name"),
            "lastname": " ".join(
                [self.partner_data.get("surname"), self.partner_data.get("lastname")]
            ),
            "email": self.partner_data.get("email"),
            "phone": self.partner_data.get("phone"),
            "address": {
                "street": self.partner_data.get("street"),
                "zip_code": self.partner_data.get("zip"),
                "city": self.partner_data.get("city"),
                "state": self.partner_data.get("subdivision"),
                "country": self.partner_data.get("country"),
            },
            "lang": self._lang(),
            "iban": self.partner_data.get("bank_iban"),
            "vat": self.partner_data.get("vat_number"),
            "payment_type": self._payment_type(),
            "nationality": self.partner_data.get("nationality"),
            "discovery_channel_id": int(self.partner_data.get("discovery_channel")),
            "sponsor_vat": self.partner_data.get("partner_number"),
            "birthdate": self.partner_data.get("birth_date").strftime("%Y-%m-%d"),
            "gender": self.partner_data.get("sex"),
            "is_company": self._is_company(),
            "voluntary_contribution": int(
                self.partner_data.get("contribute_somconnexio_option")
            ),
        }
        if self._is_company():
            sr_dict.update({
                "company_name": self._get_company_name(),
                "company_email": self.partner_data.get("email"),
            })
        return sr_dict

    def _get_company_name(self):
        if self._is_company():
            return self.partner_data.get("tradename") or self.partner_data["name"]
        else:
            return ""

    def _get_name(self):
        if self._is_company():
            return self.partner_data["name"]
        else:
            return " ".join(
                [
                    self.partner_data["name"],
                    self.partner_data["surname"],
                    self.partner_data.get("lastname"),
                ]
            )

    def _is_company(self):
        if self.partner_data.get("party_type") == "organization":
            return True
        else:
            return False

    def _type(self):
        if self.partner_data.get("partner_do_option") == "do_by_partner":
            return "sponsorship"
        return "new"

    def _payment_type(self):
        if self.partner_data.get("payment_10_terms"):
            return "split"
        return "single"

    def _lang(self):
        if self.partner_data.get("lang") == "es":
            return "es_ES"
        return "ca_ES"
