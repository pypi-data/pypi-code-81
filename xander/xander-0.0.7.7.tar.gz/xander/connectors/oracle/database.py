import cx_Oracle as oracle
import os

import pandas
from dateutil.parser import parse
from dotenv import load_dotenv

# Load environment variables
from pandas._libs.tslibs.np_datetime import OutOfBoundsDatetime

load_dotenv()


def is_date(value, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param value: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """

    try:
        # Try to parse the date
        parse(value, fuzzy=fuzzy)
        return True

    except OutOfBoundsDatetime:
        # Return false if the value is not a date
        return True

    except ValueError:
        # Return false if the value is not a date
        return False


def is_string(value):
    """
    Check if the values is a string.

    :param value: obj, value to be validated
    :return: True or False
    """

    return isinstance(value, str)


def is_number(value):
    """
    Check if the value is a number.

    :param value: obj, value to be validated
    :return: True or False
    """

    try:
        # Try to convert the value in a float number
        float(value)
        return True

    except:
        return False


class Oracle:
    """
    Database Oracle class interface.
    It contains all methods to access and query an oracle database.
    """

    def __init__(self, ip_address, port, sid, username, password, drivers):

        # Init Oracle drivers
        oracle.init_oracle_client(lib_dir=os.path.join(os.getcwd(), drivers))

        # Get the ip address of the database from the environment variables
        self.database_ip_address = ip_address

        # Get the port of the database from the environment variables
        self.database_port = port

        # Get the SID of the database from the environment variables
        self.database_sid = sid

        # Get credentials of the database from the environment variables
        self.database_username = username
        self.database_password = password

        # Init the DNS TNS
        self.dns_tns = oracle.makedsn(self.database_ip_address, self.database_port, self.database_sid)

    def fetch(self, query):
        """
        Make a query using the parameters passed by the user.

        :param query: query to be executed
        :return: (True, result) if the query is successful otherwise (False, exception)
        """

        try:
            # Connect to the database
            with oracle.connect(self.database_username, self.database_password,
                                self.dns_tns, encoding="UTF-8") as connection:

                # Initialize the connection cursor
                cursor = connection.cursor()

                # Execute the query
                cursor.execute(query)

                # Use the fetchall() to retrieve all results in batch
                rows = cursor.fetchall()

                # Return True since everything is ok, and the result of the query.
                # The result is None if it is a write query
                return rows

        except Exception as e:

            # In case of exceptions the flag is set to False
            return None

    def push(self, query):
        """
        Make a query using the parameters passed by the user.

        :param query: query to be executed
        :return: True if the query is successful otherwise False
        """

        try:
            # Connect to the database
            with oracle.connect(self.database_username, self.database_password,
                                self.dns_tns, encoding="UTF-8") as connection:

                # Initialize the connection cursor
                cursor = connection.cursor()

                # Use the cursor to execute the query
                cursor.execute(query)

                # Commit the connection, closing it
                connection.commit()

                # Return True since everything is ok, and the result of the query.
                # The result is None if it is a write query
                return True, None

        except Exception as e:

            # In case of exceotions the flag is set to False
            return False, e

    @staticmethod
    def build_insert_query(values):
        """
        Build the insert query.
        It is compatible for batch and single inserts.

        :param values: list, list of values to be inserted in the query
        :return: query formatted string
        """

        params = "("

        # For each values check its type and create the most opportune query field
        for v in values:

            # Check if it is a number
            if is_number(value=v):
                params += "{}, ".format(float(v))

            # Check if it is a date
            elif is_date(value=v):

                # Parse the date and put it in the query
                try:
                    date = pandas.to_datetime(v).strftime('%Y-%m-%d %H:%M:%S')
                    params += "TO_DATE('{}', 'YYYY-MM-DD HH24:MI:SS'), ".format(date)

                # In case the date in not valid, return null
                except OutOfBoundsDatetime:
                    params += "null, "

            # Otherwise it is considered a string
            else:
                params += "'{}', ".format(v.replace('\'', ''))

        # Remove the last two characters that are a comma and a space and close the query string
        params = params[:-2]
        params += ")"

        # Replace all numpy nan with null that is the standard missing value for Oracle DB
        params = params.replace('nan', 'null')

        return params