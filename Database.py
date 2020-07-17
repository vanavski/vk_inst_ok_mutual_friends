from vk.exceptions import VkAPIError
import vk
import requests
import psycopg2


class Database:
    def get_db(self):
        try:
            connection = psycopg2.connect(dbname="d1un08c4ikop2s",
                                          user="zbvsjseotlonov",
                                          password="92a9bc55b03b692658e5776cbce5cc8769e72d90a9806bbe824f2cec215f42ce",
                                          host="ec2-54-217-213-79.eu-west-1.compute.amazonaws.com",
                                          port="5432")

            cursor = connection.cursor()
            # Print PostgreSQL Connection properties
            print(connection.get_dsn_parameters(), "\n")

            # Print PostgreSQL version
            cursor.execute("SELECT version();")
            record = cursor.fetchone()
            print("You are connected to - ", record, "\n")

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
        finally:
            # closing database connection.
            if (connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")


    def create_table_user(self):
        try:
            connection = psycopg2.connect(dbname="d1un08c4ikop2s",
                                          user="zbvsjseotlonov",
                                          password="92a9bc55b03b692658e5776cbce5cc8769e72d90a9806bbe824f2cec215f42ce",
                                          host="ec2-54-217-213-79.eu-west-1.compute.amazonaws.com",
                                          port="5432")

            cursor = connection.cursor()

            create_table_query = '''CREATE TABLE table_user
                  (ID SERIAL PRIMARY KEY     NOT NULL,
                  user_id    TEXT    NOT NULL,
                  vk           TEXT    NOT NULL,
                  ok           TEXT    NOT NULL,
                  instagram         TEXT    NOT NULL); '''

            cursor.execute(create_table_query)
            connection.commit()
            print("Table created successfully in PostgreSQL ")

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while creating PostgreSQL table", error)
        finally:
            # closing database connection.
            if (connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")


    def create_table_vk(self):
        try:
            connection = psycopg2.connect(dbname="d1un08c4ikop2s",
                                          user="zbvsjseotlonov",
                                          password="92a9bc55b03b692658e5776cbce5cc8769e72d90a9806bbe824f2cec215f42ce",
                                          host="ec2-54-217-213-79.eu-west-1.compute.amazonaws.com",
                                          port="5432")

            cursor = connection.cursor()

            create_table_query = '''CREATE TABLE vk_tables
                  (ID SERIAL PRIMARY KEY     NOT NULL,
                  us_id    TEXT    NOT NULL,
                  vk_id    TEXT    NOT NULL,
                  table_name           TEXT    NOT NULL); '''

            cursor.execute(create_table_query)
            connection.commit()
            print("Table created successfully in PostgreSQL ")

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while creating PostgreSQL table", error)
        finally:
            # closing database connection.
            if (connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")

    def create_table_ok(self):
        try:
            connection = psycopg2.connect(dbname="d1un08c4ikop2s",
                                          user="zbvsjseotlonov",
                                          password="92a9bc55b03b692658e5776cbce5cc8769e72d90a9806bbe824f2cec215f42ce",
                                          host="ec2-54-217-213-79.eu-west-1.compute.amazonaws.com",
                                          port="5432")

            cursor = connection.cursor()

            create_table_query = '''CREATE TABLE ok_tables
                  (ID SERIAL PRIMARY KEY     NOT NULL,
                  ok_id    TEXT    NOT NULL,
                  table_name           TEXT    NOT NULL); '''

            cursor.execute(create_table_query)
            connection.commit()
            print("Table created successfully in PostgreSQL ")

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while creating PostgreSQL table", error)
        finally:
            # closing database connection.
            if (connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")

    def create_table_inst(self):
        try:
            connection = psycopg2.connect(dbname="d1un08c4ikop2s",
                                          user="zbvsjseotlonov",
                                          password="92a9bc55b03b692658e5776cbce5cc8769e72d90a9806bbe824f2cec215f42ce",
                                          host="ec2-54-217-213-79.eu-west-1.compute.amazonaws.com",
                                          port="5432")

            cursor = connection.cursor()

            create_table_query = '''CREATE TABLE inst_tables
                  (ID SERIAL PRIMARY KEY     NOT NULL,
                  inst_id    TEXT    NOT NULL,
                  table_name           TEXT    NOT NULL); '''

            cursor.execute(create_table_query)
            connection.commit()
            print("Table created successfully in PostgreSQL ")

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while creating PostgreSQL table", error)
        finally:
            # closing database connection.
            if (connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")

    def add_user_to_vk_db(self, us_id, vk_us_id):
        name = None
        is_contains = None
        try:
            connection = psycopg2.connect(dbname="d1un08c4ikop2s",
                                          user="zbvsjseotlonov",
                                          password="92a9bc55b03b692658e5776cbce5cc8769e72d90a9806bbe824f2cec215f42ce",
                                          host="ec2-54-217-213-79.eu-west-1.compute.amazonaws.com",
                                          port="5432")
            cursor = connection.cursor()

            #             check if vk_tables contains us_id sql-запрос
            #             then update-запрос
            #             else:

            name = '{}_{}_{}'.format('vk', us_id, vk_us_id)

            if (self.check_id_vk_tables(us_id, vk_us_id) == 0):
                postgres_insert_query = """ INSERT INTO vk_tables (us_id, vk_id, table_name) VALUES (%s, %s, %s)"""



                record_to_insert = (us_id, vk_us_id, name)
                cursor.execute(postgres_insert_query, record_to_insert)

                connection.commit()
                count = cursor.rowcount
                print(count, "Record inserted successfully into vk_tables table")
                is_contains = False
            else:
                is_contains = True


        except (Exception, psycopg2.Error) as error:
            if (connection):
                is_contains = True
                print("Failed to insert record into vk_tables table", error)

        finally:
            # closing database connection.
            if (connection):
                cursor.close()
                connection.close()
            print("PostgreSQL connection is closed")
            return name, is_contains


    def create_table_friends_vk(self, name):
        try:
            connection = psycopg2.connect(dbname="d1un08c4ikop2s",
                                          user="zbvsjseotlonov",
                                          password="92a9bc55b03b692658e5776cbce5cc8769e72d90a9806bbe824f2cec215f42ce",
                                          host="ec2-54-217-213-79.eu-west-1.compute.amazonaws.com",
                                          port="5432")
            cursor = connection.cursor()

            create_table_query = '''CREATE TABLE {}
                  (ID SERIAL PRIMARY KEY     NOT NULL,
                  friend_id    TEXT    NOT NULL); '''.format(name)

            cursor.execute(create_table_query)
            connection.commit()
            print("Table created successfully in PostgreSQL ")

        except (Exception, psycopg2.Error) as error:
            if (connection):
                print("Failed to insert record into {} table".format(name), error)

        finally:
            # closing database connection.
            if (connection):
                cursor.close()
                connection.close()
            print("PostgreSQL connection is closed")


    def check_id_vk_tables(self, user_id, vk_id):
        count = 0
        try:
            connection = psycopg2.connect(dbname="d1un08c4ikop2s",
                                          user="zbvsjseotlonov",
                                          password="92a9bc55b03b692658e5776cbce5cc8769e72d90a9806bbe824f2cec215f42ce",
                                          host="ec2-54-217-213-79.eu-west-1.compute.amazonaws.com",
                                          port="5432")
            cursor = connection.cursor()

            postgres_insert_query = """SELECT vk_id FROM vk_tables WHERE vk_id = '{}' and us_id = '{}'""".format(vk_id, user_id)

            cursor.execute(postgres_insert_query)

            connection.commit()
            count = cursor.rowcount
            print(count)

        except (Exception, psycopg2.Error) as error:
            if (connection):
                print("Failed command into vk_tables table", error)

        finally:
            # closing database connection.
            if (connection):
                cursor.close()
                connection.close()
            print("PostgreSQL connection is closed")
            return count

    def check_vk_user(self, us_id, vk_us_id, friends):
        name, is_contains = self.add_user_to_vk_db(us_id, vk_us_id)
        if (is_contains == False):
            self.create_table_friends_vk(name)
        self.add_friends_table_vk(name, friends, is_contains)


    def add_friends_table_vk(self, name, friends, is_contains):
        try:
            connection = psycopg2.connect(dbname="d1un08c4ikop2s",
                                          user="zbvsjseotlonov",
                                          password="92a9bc55b03b692658e5776cbce5cc8769e72d90a9806bbe824f2cec215f42ce",
                                          host="ec2-54-217-213-79.eu-west-1.compute.amazonaws.com",
                                          port="5432")
            cursor = connection.cursor()
            if (is_contains == False):
                # print
                postgres_insert_query = """ INSERT INTO {} (friend_id) VALUES """.format(name)

                for i in range(len(friends) - 1):
                    postgres_insert_query = postgres_insert_query + '({}), '.format(friends[i])

                postgres_insert_query = postgres_insert_query + '({});'.format(friends[i])
            else:
                postgres_insert_query = """ DROP TABLE {};

                                            CREATE TABLE {} (ID SERIAL PRIMARY KEY     NOT NULL,
                                            friend_id    TEXT    NOT NULL);

                                             INSERT INTO {} (friend_id) VALUES """.format(name, name, name)

                for i in range(len(friends) - 1):
                    postgres_insert_query = postgres_insert_query + '({}), '.format(friends[i])

                postgres_insert_query = postgres_insert_query + '({});'.format(friends[i])

            cursor.execute(postgres_insert_query)

            connection.commit()
            count = cursor.rowcount
            print(count, "Record inserted successfully into {} table".format(name))

        except (Exception, psycopg2.Error) as error:
            if (connection):
                print("Failed to insert record into {} table".format(name), error)
        finally:
            # closing database connection.
            if (connection):
                cursor.close()
                connection.close()
            print("PostgreSQL connection is closed")