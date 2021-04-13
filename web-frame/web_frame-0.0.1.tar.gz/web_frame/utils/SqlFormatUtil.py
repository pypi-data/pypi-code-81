import pymysql
import datetime
import decimal


def format_sql_insert(M):
    fields = []
    values = []
    for key in M.keys():
        value = M[key]
        fields.append(key)
        if type(value) == int:
            values.append(str(value))
        elif type(value) == float:
            values.append(str(value))
        elif type(value) == decimal.Decimal:
            values.append(str(value))
        elif not value:
            values.append("''")
        else:
            if type(value) == str:
                if value.startswith("ST_") or value.startswith("st_") or value.lower() == "null":
                    values.append(value)
                else:
                    values.append("'" + pymysql.escape_string(value) + "'")
            elif type(value) == datetime.datetime:
                values.append("'" + str(value) + "'")
            else:
                values.append(str(value))
    return ",".join(fields), ",".join(values)


def format_sql_update(M, table):
    fields = []
    values = []
    L = []
    for key in M.keys():
        value = M[key]
        fields.append(key)
        if type(value) == int:
            values.append(str(value))
        elif type(value) == float:
            values.append(str(value))
        elif type(value) == decimal.Decimal:
            values.append(str(value))
        elif not value:
            values.append("''")
        else:
            if type(value) == str:
                if value.startswith("ST_") or value.startswith("st_") or value.lower() == "null":
                    values.append(value)
                else:
                    values.append("'" + pymysql.escape_string(value) + "'")
            elif type(value) == datetime.datetime:
                values.append("'" + str(value) + "'")
            else:
                values.append(str(value))
        L.append('{}={}'.format(fields[-1], values[-1]))
    return ",".join(L)
