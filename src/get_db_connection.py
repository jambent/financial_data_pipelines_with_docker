from pg8000.native import Connection, DatabaseError
#from pg8000 import dbapi
from get_db_credentials import get_db_credentials


def get_db_connection(db_credentials):
    """Connect to database"""
    try:
        DB_ENDPOINT = db_credentials['endpoint']
        DB_USER = db_credentials['username']
        DB_DB = db_credentials['database']
        DB_PASSWORD = db_credentials['password']
        print(DB_ENDPOINT)
        print(DB_USER)
        print(DB_DB)
        print(DB_PASSWORD)
        # return(dbapi.connect(host=DB_ENDPOINT, user=DB_USER, 
        #                     password=DB_PASSWORD,database=DB_DB))
        return (Connection(host=DB_ENDPOINT, user=DB_USER, 
                            password=DB_PASSWORD,database=DB_DB,port=5432))
    except DatabaseError as e:
        print('Error connecting to database')
        raise e
    

if __name__ == '__main__':
    creds = get_db_credentials("db_credentials_val_data")
    #print(creds)
    conn = get_db_connection(creds)
    print(conn)
    conn.close()