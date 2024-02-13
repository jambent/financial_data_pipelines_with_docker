from pg8000.native import literal

def get_val_batch_insertion_string(date_today,batch):
    return f"""INSERT INTO val_batch 
        (date, batch, batch_ready)
        VALUES
        ({literal(date_today)}, {literal(batch)}, true);"""