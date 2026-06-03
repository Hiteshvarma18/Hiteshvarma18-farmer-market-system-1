import pandas as pd
from db import get_db

def import_csv(csv_file):

    df = pd.read_csv(csv_file)

    db = get_db()
    cursor = db.cursor()

    for _, row in df.iterrows():

        cursor.execute("""
        INSERT INTO crop_prices
        (
            crop,
            market,
            price,
            date
        )
        VALUES (%s,%s,%s,%s)
        """,
        (
            row["crop"],
            row["market"],
            row["price"],
            row["date"]
        ))

    db.commit()

    cursor.close()
    db.close()

    return len(df)