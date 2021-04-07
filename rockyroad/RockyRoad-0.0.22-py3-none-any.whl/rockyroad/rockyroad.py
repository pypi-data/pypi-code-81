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
        print(api_response)

        api_response = service.alerts().requests().list()
        print(api_response)

        api_response = service.alerts().requests().list(creator_email='user@acme.com')
        print(api_response)

        api_response = service.alerts().requests().insert(new_alert_request_json)
        print(api_response)

        api_response = service.alerts().requests().delete(brand=brand, alert_request_id=alert_request_id)
        print(api_response)

        api_response = service.alerts().reports().list()
        print(api_response)

        api_response = service.alerts().reports().list(creator_email='user@acme.com')
        print(api_response)

        api_response = service.machines().utilData().list(brand=brand, time_period='today')
        print(api_response)

        api_response = service.machines().utilData().stats().list()
        print(api_response)

        api_response = service.dealers().list()
        print(api_response)

        api_response = service.customers().list(dealer_name=dealer_name)
        print(api_response)

        api_response = service.accounts().list()
        print(api_response)

        api_response = service.accounts().list(account="c123")
        print(api_response)

        api_response = service.accounts().insert(new_account=new_account)
        print(api_response)

        api_response = service.accounts().update(account=update_account)
        print(api_response)

        api_response = service.accounts().delete(account="d123")
        print(api_response)

        api_response = service.accounts().set_is_dealer(account="d123", is_dealer=True)
        print(api_response)

        api_response = service.accounts().assign_dealer(customer_account="c123", dealer_account="d123")
        print(api_response)

        api_response = service.accounts().unassign_dealer(
            customer_account="c123", dealer_account="d123"
        )
        print(api_response)

        api_response = service.accounts().customers().list()
        print(api_response)

        api_response = service.accounts().customers().list(dealer_account="D123")
        print(api_response)

        api_response = service.accounts().dealers().list()
        print(api_response)

        api_response = service.accounts().dealers().list(customer_account="A123")
        print(api_response)



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
        print(api_response)

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

    @headers({"Ocp-Apim-Subscription-Key": key})
    class __HelloWorld(Consumer):
        def __init__(self, Resource, *args, **kw):
            super().__init__(base_url=Resource._base_url, *args, **kw)

        @returns.json
        @get("")
        def list(self):
            """This call will return Hello World."""

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

    class __Machines(object):
        """Inteface to machines resource for the RockyRoad API."""

        def __init__(self, Resource, *args, **kw):
            self._base_url = Resource._base_url

        def utilData(self):
            return self.__UtilData(self)

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
