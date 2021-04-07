
try:
    import mysql.connector
    from mysql.connector import Error
    from zcrmsdk.src.com.zoho.api.authenticator.store.token_store import TokenStore
    from zcrmsdk.src.com.zoho.api.authenticator.oauth_token import OAuthToken
    from zcrmsdk.src.com.zoho.crm.api.util.constants import Constants
    from zcrmsdk.src.com.zoho.crm.api.exception.sdk_exception import SDKException

except Exception as e:
    import mysql.connector
    from mysql.connector import Error
    from .token_store import TokenStore
    from ..oauth_token import OAuthToken
    from ....crm.api.util.constants import Constants
    from zcrmsdk.src.com.zoho.crm.api.exception.sdk_exception import SDKException


class DBStore(TokenStore):

    """
    This class to store user token details to the MySQL DataBase.
    """

    def __init__(self, host=None, database_name=None, user_name=None, password=None, port_number=None, table_name=None):

        """
        Creates a DBStore class instance with the specified parameters.

        Parameters:
            host (str) : A string containing the DataBase host name. Default value is localhost
            database_name (str) : A string containing the DataBase name. Default value is zohooauth
            user_name (str) : A string containing the DataBase user name. Default value is root
            password (str) : A string containing the DataBase password. Default value is an empty string
            port_number (str) : A string containing the DataBase port number. Default value is 3306
        """

        self.__host = host if host is not None else Constants.MYSQL_HOST
        self.__database_name = database_name if database_name is not None else Constants.MYSQL_DATABASE_NAME
        self.__user_name = user_name if user_name is not None else Constants.MYSQL_USER_NAME
        self.__password = password if password is not None else ""
        self.__port_number = port_number if port_number is not None else Constants.MYSQL_PORT_NUMBER
        self.__table_name = table_name if table_name is not None else Constants.MYSQL_TABLE_NAME

    def get_host(self):
        """
        This is a getter method to get __host.

        Returns:
            string: A string representing __host
        """

        return self.__host

    def get_database_name(self):
        """
        This is a getter method to get __database_name.

        Returns:
            string: A string representing __database_name
        """

        return self.__database_name

    def get_user_name(self):
        """
        This is a getter method to get __user_name.

        Returns:
            string: A string representing __user_name
        """

        return self.__user_name

    def get_password(self):
        """
        This is a getter method to get __password.

        Returns:
            string: A string representing __password
        """
        return self.__password

    def get_port_number(self):
        """
        This is a getter method to get __port_number.

        Returns:
            string: A string representing __port_number
        """

        return self.__port_number

    def get_table_name(self):
        """
        This is a getter method to get __table_name.

        Returns:
            string: A string representing __table_name
        """

        return self.__table_name

    def get_token(self, user, token):
        cursor = None
        try:
            connection = mysql.connector.connect(host=self.__host, database=self.__database_name, user=self.__user_name, password=self.__password, port=self.__port_number)
            try:
                if isinstance(token, OAuthToken):
                    cursor = connection.cursor()
                    query = self.construct_dbquery(user.get_email(), token, False)
                    cursor.execute(query)
                    result = cursor.fetchone()

                    if result is not None:
                        token.set_id(result[1])
                        token.set_access_token(result[6])
                        token.set_expires_in(str(result[8]))
                        token.set_refresh_token(result[5])

                        return token

            except Error as ex:
                raise ex

            finally:
                cursor.close() if cursor is not None else None
                connection.close() if connection is not None else None

        except Error as ex:
            raise SDKException(code=Constants.TOKEN_STORE, message=Constants.GET_TOKEN_DB_ERROR, cause=ex)

    def save_token(self, user, token):
        cursor = None
        try:
            connection = mysql.connector.connect(host=self.__host, database=self.__database_name, user=self.__user_name, password=self.__password, port=self.__port_number)

            try:
                if isinstance(token, OAuthToken):
                    token.set_user_mail(user.get_email())
                    self.delete_token(token)
                    cursor = connection.cursor()
                    query = "insert into oauthtoken (id,user_mail,client_id,client_secret,refresh_token,access_token,grant_token,expiry_time,redirect_url) values (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
                    val = (token.get_id(), user.get_email(), token.get_client_id(), token.get_client_secret(), token.get_refresh_token(), token.get_access_token(), token.get_grant_token(), token.get_expires_in(), token.get_redirect_url())
                    cursor.execute(query, val)
                    connection.commit()

            except Error as ex:
                raise ex

            finally:
                cursor.close() if cursor is not None else None
                connection.close() if connection is not None else None

        except Error as ex:
            raise SDKException(code=Constants.TOKEN_STORE, message=Constants.SAVE_TOKEN_DB_ERROR, cause=ex)

    def delete_token(self, token):
        cursor = None
        try:
            connection = mysql.connector.connect(host=self.__host, database=self.__database_name, user=self.__user_name, password=self.__password, port=self.__port_number)

            try:
                if isinstance(token, OAuthToken):
                    cursor = connection.cursor()
                    query = self.construct_dbquery(token.get_user_mail(), token, True)
                    cursor.execute(query)
                    connection.commit()

            except Error as ex:
                raise ex

            finally:
                cursor.close() if cursor is not None else None
                connection.close() if connection is not None else None

        except Error as ex:
            raise SDKException(code=Constants.TOKEN_STORE, message=Constants.DELETE_TOKEN_DB_ERROR, cause=ex)

    def get_tokens(self):
        cursor = None
        try:
            connection = mysql.connector.connect(host=self.__host, database=self.__database_name, user=self.__user_name, password=self.__password, port=self.__port_number)
            tokens = []

            try:
                cursor = connection.cursor()
                query = 'select * from ' + self.__table_name + ";"
                cursor.execute(query)
                results = cursor.fetchall()

                for result in results:
                    grant_token = None

                    if result[7] is not None and result[7] != Constants.NULL_VALUE and len(result[7]) > 0:
                        grant_token = result[7]

                    token = OAuthToken(client_id=result[3], client_secret=None, grant_token=grant_token, refresh_token=result[5])
                    token.set_id(result[1])
                    token.set_expires_in(str(result[8]))
                    token.set_user_mail(result[2])
                    token.set_access_token(result[6])
                    tokens.append(token)

                return tokens

            except Error as ex:
                raise ex

            finally:
                cursor.close() if cursor is not None else None
                connection.close() if connection is not None else None

        except Error as ex:
            raise SDKException(Constants.TOKEN_STORE, Constants.GET_TOKENS_DB_ERROR, None, ex)

    def delete_tokens(self):
        cursor = None
        try:
            connection = mysql.connector.connect(host=self.__host, database=self.__database_name, user=self.__user_name, password=self.__password, port=self.__port_number)

            try:
                cursor = connection.cursor()
                query = 'delete from ' + self.__table_name + ";"
                cursor.execute(query)
                connection.commit()

            except Error as ex:
                raise ex

            finally:
                cursor.close() if cursor is not None else None
                connection.close() if connection is not None else None
        except Error as ex:
            raise SDKException(Constants.TOKEN_STORE, Constants.DELETE_TOKENS_DB_ERROR, Exception=ex)

    def get_token_by_id(self, id, token):
        cursor = None
        try:
            connection = mysql.connector.connect(host=self.__host, database=self.__database_name, user=self.__user_name, password=self.__password, port=self.__port_number)
            try:
                if isinstance(token, OAuthToken):

                    query = "select * from " + self.__table_name + " where id='" + id + "'"
                    cursor = connection.cursor()
                    cursor.execute(query)
                    results = cursor.fetchall()

                    for result in results:
                        if result[1] == id:
                            token = OAuthToken(client_id=result[3], client_secret=result[4], redirect_url=result[9], grant_token=result[7], refresh_token=result[5])
                            token.set_id(result[1])
                            token.set_access_token(result[6])
                            token.set_expires_in(str(result[8]))
                            token.set_user_mail(result[2])
                            return token

            except Error as ex:
                raise ex

            finally:
                cursor.close() if cursor is not None else None
                connection.close() if connection is not None else None

        except Error as ex:
            raise SDKException(code=Constants.TOKEN_STORE, message=Constants.GET_TOKEN_BY_ID_DB_ERROR, cause=ex)

    def construct_dbquery(self, email, token, is_delete):
        if email is None:
            raise SDKException(Constants.USER_MAIL_NULL_ERROR, Constants.USER_MAIL_NULL_ERROR_MESSAGE)

        query = "delete from " if is_delete is True else "select * from "
        query += self.__table_name + " where user_mail ='" + email + "' and client_id='" + token.get_client_id() + "' and "

        if token.get_grant_token() is not None:
            query += "grant_token='" + token.get_grant_token() + "'"

        else:
            query += "refresh_token='" + token.get_refresh_token() + "'"

        return query
