import mysql.connector as connector  # libraries


class Database_class:  # class for connection with mysql database
    def __init__(self):  # init database connection
        self.__dsn = {  # details for connecting to database
            "host": "localhost",
            "user": "user_local",
            "passwd": "user_local",
            "db": "weatherstation_db"
        }

    def get_data_from_database(self, table_name):  # get all data from table
        self.__connection = connector.connect(**self.__dsn)  # define connection
        self.__cursor = self.__connection.cursor()  # connect with database

        query = "SELECT * FROM %s" % table_name  # query
        self.__cursor.execute(query)  # execute query
        result = self.__cursor.fetchall()  # get all data
        self.__cursor.close()  # close database connection
        return result

    def get_time_and_measurement_from_weatherstation(self, time_hour, type_measurement):  # get time and value from table weatherstation
        self.__connection = connector.connect(**self.__dsn)  # define connection
        self.__cursor = self.__connection.cursor()  # connect with database

        # query
        query = "SELECT weatherstation.TIME, measurement.Value " \
                "FROM weatherstation " \
                "JOIN measurement ON measurement.ID = weatherstation.ID_measurement " \
                "JOIN type ON type.ID = measurement.ID_type " \
                "WHERE hour(weatherstation.Time) BETWEEN '%d' - 1 AND '%d' + 1 AND type.ID = '%d'" \
                % (time_hour, time_hour, type_measurement)
        self.__cursor.execute(query)  # execute query
        result = self.__cursor.fetchall()  # get all data
        self.__cursor.close()  # close database connection

        lst_time = []  # list for time
        lst_value = []  # list for measurements
        lst_result = []  # list for result
        for index in range(0, len(result)):  # go trough every tuple in query result
            lst_time.append(result[index][0])  # add time part of the tuple to list time
            lst_value.append(result[index][1])  # add measurement part of the tuple to list value
        lst_result.append(lst_time)  # add list time to list result
        lst_result.append(lst_value)  # add list value to list result
        return lst_result  # return list result

    def set_data_to_table_measurement(self, value, id_type):  # send data to table measurement
        self.__connection = connector.connect(**self.__dsn)  # define connection
        self.__cursor = self.__connection.cursor()  # connect with database

        # query
        query = "INSERT INTO measurement (Value , ID_type)" \
                "VALUES ('%.2f','%d')" % (value, id_type)
        self.__cursor.execute(query)  # execute query
        self.__connection.commit()  # save changes in database
        self.__cursor.close()  # close database connection

    def set_data_to_table_type(self, description):  # send data to table type
        self.__connection = connector.connect(**self.__dsn)  # define connection
        self.__cursor = self.__connection.cursor()  # connect with database

        # query
        query = "INSERT INTO type (Description) VALUES ('%s')" % (description)
        self.__cursor.execute(query)  # execute query
        self.__connection.commit()  # save changes in database
        self.__cursor.close()  # close database connection

    def set_data_to_table_weatherstation(self, time, id_measurement):  # send data to table weatherstation
        self.__connection = connector.connect(**self.__dsn)  # define connection
        self.__cursor = self.__connection.cursor()  # connect with database

        # query
        query = "INSERT INTO weatherstation (Time, ID_measurement)" \
                "VALUES ('%s','%d')" % (time, id_measurement)
        self.__cursor.execute(query)  # execute query
        self.__connection.commit()  # save changes in database
        self.__cursor.close()  # close database connection

    def truncate_table(self, table_name):  # delete all data from table
        self.__connection = connector.connect(**self.__dsn)  # define connection
        self.__cursor = self.__connection.cursor()  # connect with database

        query = "TRUNCATE TABLE %s" % table_name  # query
        self.__cursor.execute(query)  # execute query
        self.__connection.commit()  # save changes in database
        self.__cursor.close()  # close database connection
