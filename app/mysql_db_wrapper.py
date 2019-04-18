import mysql.connector


class MysqlObject:
    def __init__(self, user, password, db_name):
        self.config = {'user': user, 'password': password, 'host': 'mysql', 'port': '3306', 'database': db_name}
        try:
            self.connection = mysql.connector.connect(**self.config)
        except Exception as e:
            raise Exception("unable to connect to mysql db with user {}, password {} and db name {} - {}".format(user, password, db_name, e))

    def query_db(self, sql_query):
        query_results = []
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql_query)
            query_results = cursor.fetchall()
            cursor.close()
        except Exception as e:
            print("unable to query db with sql statement {} - {}".format(sql_query, e))

        return query_results

    def insert_row(self, sql_query, query_values):
        returned_id = -1
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql_query, query_values)
            self.connection.commit()
            returned_id = cursor.lastrowid
            cursor.close()
        except Exception as e:
            print("unable to insert sql statement {} with values {} - {}".format(sql_query, query_values, e))

        return returned_id

    def close_connection(self):
        try:
            self.connection.close()
        except Exception as e:
            print("unable to close mysql connection - {}".format(e))
