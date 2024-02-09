from pg8000.native import Connection, DatabaseError
import ssl
#from src.utilities.get_db_credentials import get_db_credentials


def get_db_connection(db_credentials):
    """Connect to database"""
    try:
        DB_ENDPOINT = db_credentials['endpoint']
        DB_USER = db_credentials['username']
        DB_DB = db_credentials['database']
        DB_PASSWORD = db_credentials['password']

        ssl_context = ssl.SSLContext()
        return (Connection(host=DB_ENDPOINT, user=DB_USER, 
                            password=DB_PASSWORD,database=DB_DB,ssl_context=ssl_context))
    except DatabaseError as e:
        print('Error connecting to database')
        raise e