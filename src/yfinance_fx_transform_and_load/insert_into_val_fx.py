import awswrangler as wr

def insert_into_val_fx(dataframe, db_connection):
  wr.postgresql.to_sql(
            df=dataframe,
            table='val_fx',
            schema='public',
            con=db_connection,
            mode='upsert',
            index=False,
            use_column_names=True,
            upsert_conflict_columns=['id']
        )