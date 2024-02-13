import ssl
import awswrangler as wr

def new_db_connection():
    ssl_context = ssl.SSLContext()
    conn = wr.postgresql.connect(secret_id="db_credentials_val_data",ssl_context=ssl_context)
    return conn