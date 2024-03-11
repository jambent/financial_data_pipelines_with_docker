import awswrangler as wr
import ssl

if __name__ == '__main__':
    ssl_context = ssl.SSLContext()
    conn = wr.postgresql.connect(
        secret_id="db_credentials_val_data",
        ssl_context=ssl_context)
    cursor = conn.cursor()

    try:
        create_val_fx = """CREATE TABLE val_fx (
        id SERIAL PRIMARY KEY,
        date DATE,
        batch VARCHAR,
        domestic_ccy VARCHAR,
        foreign_ccy VARCHAR,
        fx_rate DECIMAL(13,8),
        inserted TIMESTAMP default CURRENT_TIMESTAMP
        );"""

        create_val_equity_index = """CREATE TABLE val_equity_index (
        id SERIAL PRIMARY KEY,
        date DATE,
        batch VARCHAR,
        equity_index VARCHAR,
        index_level DECIMAL(13,8),
        inserted TIMESTAMP default CURRENT_TIMESTAMP
        );"""

        create_val_batch = """CREATE TABLE val_batch (
        id SERIAL PRIMARY KEY,
        date DATE,
        batch VARCHAR,
        batch_ready BOOLEAN,
        inserted TIMESTAMP default CURRENT_TIMESTAMP
        );"""

        cursor.execute(create_val_fx)
        cursor.execute(create_val_equity_index)
        cursor.execute(create_val_batch)
        conn.commit()

    finally:
        conn.close()
