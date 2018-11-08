from psycopg2 import connect


def create_connection():
    '''This method creates connection to database'''
    cnx = connect(
        user="postgres",
        password="coderslab",
        host="localhost",
        database="cinema_assistant")

    cnx.autocommit = True
    cursor = cnx.cursor()

    return cnx, cursor


def close_connection(cnx, cursor):
    '''Closing conneciton with database'''
    cursor.close()
    cnx.close()
