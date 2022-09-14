from pymysql import *


class DatabaseHelper():
    USER = 'simran'
    PASSWORD = 'simran'
    HOST = 'localhost'
    database = 'world'

    @classmethod
    def get_columns(cls, description):
        # column names are present as the first element of the collection,
        # hence extract the first element[0], create tuple & return it.
        return tuple(map(lambda x: x[0], description))

    @classmethod
    def get_data(cls, query, parameters=None) -> dict:
        conn = connect(host=cls.HOST, database=cls.database, user=cls.USER, password=cls.PASSWORD)
        cur = conn.cursor(cursor=cursors.DictCursor)
        if (parameters is None):
            cur.execute(query)
        else:
            cur.execute(query, parameters)
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result

    @classmethod
    # returns me multiple rows as tuple inside a tuple
    def get_all_data(cls, query, parameters=None):
        conn = connect(host=cls.HOST, database=cls.database, user=cls.USER, password=cls.PASSWORD)
        cur = conn.cursor()
        if (parameters is None):
            cur.execute(query)
        else:
            cur.execute(query, parameters)
        result = cur.fetchall()
        # get me the column names of the data
        headers = DatabaseHelper.get_columns(cur.description)
        cur.close()
        conn.close()
        # add the columns as the first row of my data
        return (headers,) + result

    @classmethod
    # insert, update, delete
    def execute_query(cls, query, parameters=None):
        conn = connect(host=cls.HOST, database=cls.database, user=cls.USER, password=cls.PASSWORD)
        cur = conn.cursor()
        if (parameters is None):
            cur.execute(query)
        else:
            cur.execute(query, parameters)
        conn.commit()
        cur.close()
        conn.close()

    @classmethod
    def get_all_data_multiple_input(cls, query, params):
        conn = connect(host=cls.HOST, database=cls.database, user=cls.USER, password=cls.PASSWORD)
        cur = conn.cursor()
        format_strings = ','.join(['%s'] * len(params))
        cur.execute(query % format_strings, params)
        result = cur.fetchall()
        # get me the column names of the data
        headers = DatabaseHelper.get_columns(cur.description)
        cur.close()
        conn.close()
        # add the columns as the first row of my data
        return (headers,) + result

    @classmethod
    def execute_all_data_multiple_input(cls, query, params):
        conn = connect(host=cls.HOST, database=cls.database, user=cls.USER, password=cls.PASSWORD)
        cur = conn.cursor()
        format_strings = ','.join(['%s'] * len(params))
        cur.execute(query % format_strings, params)
        conn.commit()
        cur.close()
        conn.close()
