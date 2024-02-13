import ssl
import awswrangler as wr
from pg8000.native import literal
from datetime import timedelta, datetime as dt

if __name__ == '__main__':

    time_now = dt.now()
    date_today = str(time_now.date())
    print(date_today)
    ssl_context = ssl.SSLContext()

    conn = wr.postgresql.connect(
        secret_id="db_credentials_val_data",
        ssl_context=ssl_context)
    cursor = conn.cursor()
    try:
        activate_1630_val_batch = f"""INSERT INTO val_batch 
        (date, batch, batch_ready)
        VALUES
        ({literal(date_today)}, '1630', true);"""

        print(activate_1630_val_batch)
        cursor.execute(activate_1630_val_batch)
        conn.commit()
    finally:
        conn.close()