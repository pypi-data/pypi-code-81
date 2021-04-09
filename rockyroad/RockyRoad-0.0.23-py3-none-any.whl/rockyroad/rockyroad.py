from uplink import (
    Consumer,
    get,
    post,
    patch,
    delete,
    returns,
    headers,
    Body,
    json,
    Query,
)
import os

try:
    key = os.environ["OCP_APIM_SUBSCRIPTION_KEY"]
except KeyError as e:
    print(
        f"""ERROR: Define the environment variable {e} with your subscription key.  For example:

    export OCP_APIM_SUBSCRIPTION_KEY="INSERT_YOUR_SUBSCRIPTION_KEY"

    """
    )
    key = None


def build(serviceName, version, base_url, **kw):
    """Returns a resource to interface with the RockyRoad API.

    Usage Examples - Data Services:

        from rockyroad.rockyroad import build

        service = build(serviceName="data-services", version="v1", base_url='INSERT_URL_FOR_API')

        api_response = service.helloWorld().list()

        service.docs().swagger().content
        service.docs().redocs().content
        service.docs().openapi()

        api_response = service.alerts().requests().list()
        api_response = service.alerts().requests().list(creator_email='user@acme.com')
        api_response = service.alerts().requests().insert(new_alert_request_json)
        api_response = service.alerts().requests().delete(brand=brand, alert_request_id=alert_request_id)

        api_response = service.alerts().reports().list()
        api_response = service.alerts().reports().list(creator_email='user@acme.com')

        api_response = service.machines().utilData().list(brand=brand, time_period='today')
        api_response = service.machines().utilData().stats().list()

        api_response = service.dealers().list()
        api_response = service.customers().list(dealer_name=dealer_name)

        api_response = service.accounts().list()
        api_response = service.accounts().list(account="c123")
        api_response = service.accounts().insert(new_account=new_account)
        api_response = service.accounts().update(account=update_account)

        api_response = service.accounts().delete(account="d123")
        api_response = service.accounts().set_is_dealer(account="d123", is_dealer=True)
        api_response = service.accounts().assign_dealer(customer_account="c123", dealer_account="d123")
        api_response = service.accounts().unassign_dealer(customer_account="c123", dealer_account="d123")

        api_response = service.accounts().customers().list()
        api_response = service.accounts().customers().list(dealer_account="D123")

        api_response = service.accounts().dealers().list()
        api_response = service.accounts().dealers().list(customer_account="A123")

        api_response = service.apbs().list()
        api_response = service.apbs().list(apb_id=6)
        api_response = service.apbs().list(brand="brand", model="model", serial="1234")

        api_response = service.apbs().insert(new_apb=new_apb)
        api_response = service.apbs().delete(apb_id=7)
        api_response = service.apbs().update(apb=updated_apb)

        api_response = service.apbs().status().list(apb_id=8)
        api_response = service.apbs().status().insert(new_apb_status=new_apb_status)
        api_response = service.apbs().status().delete(apb_id=8, apb_status_id=19)
        api_response = service.apbs().status().update(apb_status=updated_apb_status)

        api_response = service.machines().catalog().list()
        api_response = service.machines().catalog().list(machine_catalog_id=3)
        api_response = service.machines().catalog().insert(new_machine_catalog=new_machine_catalog)
        api_response = service.machines().catalog().delete(machine_catalog_id=4)
        api_response = service.machines().catalog().update(machine_catalog=machine_catalog)

        api_response = service.machines().list()
        api_response = service.machines().list(account="a123")
        api_response = service.machines().list(brand="brand", model="model", serial="1234")
        api_response = service.machines().insert(new_machine=new_machine)
        api_response = service.machines().delete(machine_id=10)
        api_response = service.machines().update(machine=updated_machine)

    Usage Examples - Email Services:

        from rockyroad.rockyroad import build

        service = build(serviceName="email-services", version="v1", base_url='INSERT_URL_FOR_API')

        email_message = {
            "recipient": "someone@acme.com",
            "subject": "Sending Email Message via API",
            "html_message": "This email send via the API!",
            "text_message": "This email send via the API!",
            }

        api_response = service.emails().send(email_message_json)


    """
    try:
        service = {
            "data-services": DataServicesResource,
            "email-services": EmailServicesResource,
        }[serviceName]
        return service(
            serviceName=serviceName,
            version=version,
            base_url=base_url,
            test=kw.get("test", False),
        )
    except KeyError:
        print(
            f"ERROR:  The service name '{serviceName}' was not found or is not supported."
        )


class DataServicesResource(object):
    """Inteface to Data Services resources for the RockyRoad API."""

    def __init__(self, *args, **kw):
        base_url = kw["base_url"]
        serviceName = kw["serviceName"]
        version = kw["version"]
        test = kw["test"]
        if test:
            api_base_url = base_url + "/"
        else:
            api_base_url = base_url + "/" + serviceName + "/" + version + "/"
        self._base_url = api_base_url

    def helloWorld(self):
        return self.__HelloWorld(self)

    def docs(self):
        return self.__Docs(self)

    def alerts(self):
        return self.__Alerts(self)

    def machines(self):
        return self.__Machines(self)

    def dealers(self):
        return self.__Dealers(self)

    def customers(self):
        return self.__Customers(self)

    def accounts(self):
        return self.__Accounts(self)

    def apbs(self):
        return self.__Apbs(self)

    @headers({"Ocp-Apim-Subscription-Key": key})
    class __HelloWorld(Consumer):
        def __init__(self, Resource, *args, **kw):
            super().__init__(base_url=Resource._base_url, *args, **kw)

        @returns.json
        @get("")
        def list(self):
            """This call will return Hello World."""

    @headers({"Ocp-Apim-Subscription-Key": key})
    class __Docs(Consumer):
        def __init__(self, Resource, *args, **kw):
            super().__init__(base_url=Resource._base_url, *args, **kw)

        @get("docs/swagger")
        def swagger(self):
            """This call will return swagger ui."""

        @get("docs/redocs")
        def redocs(self):
            """This call will return redoc ui."""

        @returns.json
        @get("docs/openapi.json")
        def openapi(self):
            """This call will return OpenAPI json."""

    class __Alerts(object):
        """Inteface to alerts resource for the RockyRoad API."""

        def __init__(self, Resource, *args, **kw):
            self._base_url = Resource._base_url

        def requests(self):
            return self.__Requests(self)

        def reports(self):
            return self.__Reports(self)

        @headers({"Ocp-Apim-Subscription-Key": key})
        class __Requests(Consumer):
            """Inteface to alert requests resource for the RockyRoad API."""

            def __init__(self, Resource, *args, **kw):
                super().__init__(base_url=Resource._base_url, *args, **kw)

            @returns.json
            @get("alerts/requests")
            def list(self, creator_email: Query = None):
                """This call will return detailed alert request information for the creator's email specified or all alert requests if no email is specified."""

            @returns.json
            @json
            @post("alerts/requests")
            def insert(self, new_alert_request: Body):
                """This call will create an alert request with the specified parameters."""

            @returns.json
            @delete("alerts/requests")
            def delete(self, brand: Query(type=str), alert_request_id: Query(type=int)):
                """This call will delete the alert request for the specified brand and alert request id."""

        @headers({"Ocp-Apim-Subscription-Key": key})
        class __Reports(Consumer):
            """Inteface to alert reports resource for the RockyRoad API."""

            def __init__(self, Resource, *args, **kw):
                super().__init__(base_url=Resource._base_url, *args, **kw)

            @returns.json
            @get("alerts/reports")
            def list(self, creator_email: Query = None):
                """This call will return detailed alert report information for the creator's email specified or all alert reports if no email is specified."""

    @headers({"Ocp-Apim-Subscription-Key": key})
    class __Machines(Consumer):
        """Inteface to machines resource for the RockyRoad API."""

        def __init__(self, Resource, *args, **kw):
            self._base_url = Resource._base_url
            super().__init__(base_url=Resource._base_url, *args, **kw)

        def utilData(self):
            return self.__UtilData(self)

        def catalog(self):
            return self.__Catalog(self)

        @returns.json
        @get("machines")
        def list(
            self,
            brand: Query(type=str) = None,
            model: Query(type=str) = None,
            serial: Query(type=str) = None,
            account: Query(type=str) = None,
        ):
            """This call will return machine information for the machine or account specified or all machines if nothing is specified."""

        @returns.json
        @json
        @post("machines")
        def insert(self, new_machine: Body):
            """This call will create an APB with the specified parameters."""

        @returns.json
        @delete("machines")
        def delete(self, machine_id: Query(type=int)):
            """This call will delete the machine for the specified id."""

        @returns.json
        @json
        @patch("machines")
        def update(self, machine: Body):
            """This call will update the machine with the specified parameters."""

        @headers({"Ocp-Apim-Subscription-Key": key})
        class __Catalog(Consumer):
            """Inteface to Machine Catalog resource for the RockyRoad API."""

            def __init__(self, Resource, *args, **kw):
                super().__init__(base_url=Resource._base_url, *args, **kw)

            @returns.json
            @get("machines/catalog")
            def list(self, machine_catalog_id: Query(type=int) = None):
                """This call will return detailed machine catalog information for the id specified or all machine catalog information if id is specified."""

            @returns.json
            @json
            @post("machines/catalog")
            def insert(self, new_machine_catalog: Body):
                """This call will create a Machine Catalog entry with the specified parameters."""

            @returns.json
            @delete("machines/catalog")
            def delete(self, machine_catalog_id: Query(type=int)):
                """This call will delete the Machine Catalog entry for the specified Machine Catalog id."""

            @returns.json
            @json
            @patch("machines/catalog")
            def update(self, machine_catalog: Body):
                """This call will update the Machine Catalog with the specified parameters."""

        @headers({"Ocp-Apim-Subscription-Key": key})
        class __UtilData(Consumer):
            """Inteface to machine utildata resource for the RockyRoad API."""

            def __init__(self, Resource, *args, **kw):
                super().__init__(base_url=Resource._base_url, *args, **kw)
                self._base_url = Resource._base_url

            def stats(self):
                return self.__Stats(self)

            @returns.json
            @get("machines/util-data")
            def list(self, brand: Query(type=str), time_period: Query(type=str)):
                """This call will return utilization data for the time period specified in the query parameter."""

            @headers({"Ocp-Apim-Subscription-Key": key})
            class __Stats(Consumer):
                """Inteface to utildata stats resource for the RockyRoad API."""

                def __init__(self, Resource, *args, **kw):
                    super().__init__(base_url=Resource._base_url, *args, **kw)

                @returns.json
                @get("machines/util-data/stats")
                def list(self):
                    """This call will return stats for the utildatastatus table."""

    @headers({"Ocp-Apim-Subscription-Key": key})
    class __Dealers(Consumer):
        def __init__(self, Resource, *args, **kw):
            super().__init__(base_url=Resource._base_url, *args, **kw)

        @returns.json
        @get("dealers")
        def list(self):
            """This call will return a list of dealers."""

    @headers({"Ocp-Apim-Subscription-Key": key})
    class __Customers(Consumer):
        def __init__(self, Resource, *args, **kw):
            super().__init__(base_url=Resource._base_url, *args, **kw)

        @returns.json
        @get("customers")
        def list(self, dealer_name: Query(type=str)):
            """This call will return a list of customers and machines supported by the specified dealer."""

    @headers({"Ocp-Apim-Subscription-Key": key})
    class __Accounts(Consumer):
        """Inteface to accounts resource for the RockyRoad API."""

        def __init__(self, Resource, *args, **kw):
            self._base_url = Resource._base_url
            super().__init__(base_url=Resource._base_url, *args, **kw)

        def dealers(self):
            return self.__Dealers(self)

        def customers(self):
            return self.__Customers(self)

        @returns.json
        @get("accounts")
        def list(self, account: Query = None):
            """This call will return detailed alert request information for the creator's email specified or all alert requests if no email is specified."""

        @returns.json
        @delete("accounts")
        def delete(self, account: Query(type=str)):
            """This call will delete the alert request for the specified brand and alert request id."""

        @returns.json
        @json
        @post("accounts")
        def insert(self, new_account: Body):
            """This call will create an alert request with the specified parameters."""

        @returns.json
        @json
        @patch("accounts")
        def update(self, account: Body):
            """This call will create an alert request with the specified parameters."""

        @returns.json
        @json
        @post("accounts/assign-dealer")
        def assign_dealer(
            self, customer_account: Query(type=str), dealer_account: Query(type=str)
        ):
            """This call will create an alert request with the specified parameters."""

        @returns.json
        @json
        @post("accounts/unassign-dealer")
        def unassign_dealer(
            self, customer_account: Query(type=str), dealer_account: Query(type=str)
        ):
            """This call will create an alert request with the specified parameters."""

        @returns.json
        @json
        @post("accounts/set-is-dealer")
        def set_is_dealer(self, account: Query(type=str), is_dealer: Query(type=bool)):
            """This call will create an alert request with the specified parameters."""

        @headers({"Ocp-Apim-Subscription-Key": key})
        class __Customers(Consumer):
            """Inteface to customers requests resource for the RockyRoad API."""

            def __init__(self, Resource, *args, **kw):
                super().__init__(base_url=Resource._base_url, *args, **kw)

            @returns.json
            @get("accounts/customers")
            def list(self, dealer_account: Query(type=str) = None):
                """This call will return detailed alert request information for the creator's email specified or all alert requests if no email is specified."""

        @headers({"Ocp-Apim-Subscription-Key": key})
        class __Dealers(Consumer):
            """Inteface to dealers resource for the RockyRoad API."""

            def __init__(self, Resource, *args, **kw):
                super().__init__(base_url=Resource._base_url, *args, **kw)

            @returns.json
            @get("accounts/dealers")
            def list(self, customer_account: Query(type=str) = None):
                """This call will return detailed alert request information for the creator's email specified or all alert requests if no email is specified."""

    @headers({"Ocp-Apim-Subscription-Key": key})
    class __Apbs(Consumer):
        """Inteface to APBs resource for the RockyRoad API."""

        def __init__(self, Resource, *args, **kw):
            self._base_url = Resource._base_url
            super().__init__(base_url=Resource._base_url, *args, **kw)

        def status(self):
            return self.__Status(self)

        @returns.json
        @get("apbs")
        def list(
            self,
            apb_id: Query(type=int) = None,
            account: Query(type=str) = None,
            list_apbs_for_dealer_supported_accounts: Query(type=bool) = None,
            brand: Query(type=str) = None,
            model: Query(type=str) = None,
            serial: Query(type=str) = None,
        ):
            """This call will return detailed APB information for the apb or machine specified or all APBs if nothing is specified."""

        @returns.json
        @json
        @post("apbs")
        def insert(self, new_apb: Body):
            """This call will create an APB with the specified parameters."""

        @returns.json
        @delete("apbs")
        def delete(self, apb_id: Query(type=int)):
            """This call will delete the APB for the specified APB id."""

        @returns.json
        @json
        @patch("apbs")
        def update(self, apb: Body):
            """This call will update the APB with the specified parameters."""

        @headers({"Ocp-Apim-Subscription-Key": key})
        class __Status(Consumer):
            """Inteface to APB Status resource for the RockyRoad API."""

            def __init__(self, Resource, *args, **kw):
                super().__init__(base_url=Resource._base_url, *args, **kw)

            @returns.json
            @get("apbs/status")
            def list(self, apb_id: Query(type=int) = None):
                """This call will return detailed alert request information for the creator's email specified or all alert requests if no email is specified."""

            @returns.json
            @delete("apbs/status")
            def delete(self, apb_id: Query(type=int), apb_status_id: Query(type=int)):
                """This call will delete the APB Status for the specified APB Status id."""

            @returns.json
            @json
            @post("apbs/status")
            def insert(self, new_apb_status: Body):
                """This call will create an alert request with the specified parameters."""

            @returns.json
            @json
            @patch("apbs/status")
            def update(self, apb_status: Body):
                """This call will update the APB status with the specified parameters."""


class EmailServicesResource(object):
    """Inteface to Data Services resources for the RockyRoad API."""

    def __init__(self, *args, **kw):
        base_url = kw["base_url"]
        serviceName = kw["serviceName"]
        version = kw["version"]
        test = kw["test"]
        if test:
            api_base_url = base_url + "/"
        else:
            api_base_url = base_url + "/" + serviceName + "/" + version + "/"
        self._base_url = api_base_url

    def emails(self):
        return self.__Emails(self)

    @headers({"Ocp-Apim-Subscription-Key": key})
    class __Emails(Consumer):
        def __init__(self, Resource, *args, **kw):
            super().__init__(base_url=Resource._base_url, *args, **kw)

        @returns.json
        @json
        @post("manual/paths/invoke")
        def send(self, email_message: Body):
            """This call will send an email message with the specified recipient, subject, and html/text body."""
