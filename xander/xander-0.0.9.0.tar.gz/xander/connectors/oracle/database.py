import multiprocessing

import cx_Oracle as oracle
import os
import numpy as np
import pandas
from dotenv import load_dotenv

# Load environment variables
from joblib import Parallel, delayed
from tqdm import tqdm

load_dotenv()


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

        n_jobs = multiprocessing.cpu_count()

        def process_data(line):
            return tuple([v if not (pandas.isna(v) or v is np.nan) else None for v in line])

        data = []
        for i in tqdm(range(0, len(dataset), batch_size), total=np.ceil(len(dataset)) / batch_size):

            d = Parallel(n_jobs=n_jobs)(delayed(process_data)(dataset.values[j]) for j in
                tqdm(dataset.values[i:i + batch_size], total=len(dataset.values[i:i + batch_size])))
            data.append(d)

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
                sql = f"INSERT INTO {table} {columns} VALUES {placeholder}"

                # For each data batch make the write query
                for bundle in tqdm(data, total=len(data)):
                    cursor.executemany(sql, bundle)

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
            if 'date' in list(dataset.columns)[i - 1].lower() or 'data' in list(dataset.columns)[i - 1].lower() \
                    or 'anno' in list(dataset.columns)[i - 1].lower():

                placeholder.append(f"TO_DATE(:{i}, 'YYYY-MM-DD HH24:MI:SS')")
            else:
                placeholder.append(f':{i}')
        placeholder = "(" + ", ".join(placeholder) + ")"

        return placeholder
