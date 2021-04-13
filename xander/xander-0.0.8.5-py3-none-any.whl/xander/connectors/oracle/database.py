import cx_Oracle as oracle
import os
import numpy as np
import pandas
from dateutil.parser import parse
from dotenv import load_dotenv

# Load environment variables
from pandas._libs.tslibs.np_datetime import OutOfBoundsDatetime
from tqdm import tqdm

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

        # Connect to the database
        with oracle.connect(self.database_username, self.database_password, self.dns_tns,
                            encoding="UTF-8") as connection:
            try:

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

                # Commit the connection, closing it
                connection.commit()

                # In case of exceptions the flag is set to False
                return False, e

    def push_many(self, table, dataset, batch_size=50000):
        """
        Make a batch insert query in the specified database.

        @param table: table name
        @param dataset: dataset to be inserted
        @param batch_size: batch size of the query
        @return: True or False
        """

        current_index = 0

        while current_index < len(dataset) - 1:

            # Connect to the database
            with oracle.connect(self.database_username, self.database_password, self.dns_tns,
                                encoding="UTF-8") as connection:
                try:
                    # Initialize the connection cursor
                    cursor = connection.cursor()

                    # Create the list of columns to be placed in the query string
                    columns = str(tuple(dataset.columns)).replace('\'', '').replace('/', '_')

                    # Create the list of placeholders to be places in the query string
                    placeholder = self.create_placeholders(dataset)

                    # Generate the SQL statement
                    sql = f"insert into {table} {columns} values {placeholder}"

                    data = []
                    for i, line in tqdm(enumerate(dataset.values), total=len(dataset)):

                        if i < current_index:
                            continue

                        current_index += 1

                        # Create the tuple of values
                        data.append(tuple([v if not (pandas.isna(v) or v is np.nan) else None for v in line]))

                        # Makes the query when the batch size is reached
                        if len(data) % batch_size == 0:
                            cursor.executemany(sql, data)
                            data = []

                    # Execute the query if some data remains out
                    if data:
                        cursor.executemany(sql, data)

                    # Commit the connection, closing it
                    connection.commit()

                    # Return True since everything is ok, and the result of the query.
                    # The result is None if it is a write query
                    return True, None

                except Exception as e:
                    # Commit the connection, closing it
                    connection.commit()

                    # In case of exceptions the flag is set to False
                    return False, e

    @staticmethod
    def create_placeholders(dataset):
        """
        Create the list of placeholders for the batch insert query.

        @param dataset: target dataset
        @return: list of placeholders
        """

        placeholder = []
        for i in range(1, len(dataset.columns) + 1):
            if 'date' in list(dataset.columns)[i - 1].lower() or 'data' in list(dataset.columns)[i - 1].lower()\
                    or 'anno' in list(dataset.columns)[i - 1].lower():

                placeholder.append(f"TO_DATE(:{i}, 'YYYY-MM-DD HH24:MI:SS')")
            else:
                placeholder.append(f':{i}')
        placeholder = "(" + ", ".join(placeholder) + ")"

        return placeholder

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
