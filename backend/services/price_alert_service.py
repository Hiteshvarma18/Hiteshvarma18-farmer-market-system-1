from db import get_db

def detect_price_alerts(threshold=5):

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT crop, market, price, date
        FROM crop_prices
        ORDER BY crop, market, date ASC
    """)

    rows = cursor.fetchall()

    cursor.close()
    db.close()

    alerts = []

    prev = {}

    for row in rows:

        key = (row["crop"], row["market"])

        if key in prev:

            old_price = prev[key]
            new_price = row["price"]

            change = float(new_price) - float(old_price)

            if abs(change) >= threshold:

                direction = "increased 📈" if change > 0 else "decreased 📉"

                alerts.append({
                    "crop": row["crop"],
                    "market": row["market"],
                    "message": f"{row['crop']} price {direction} in {row['market']} by {abs(change)}"
                })

        prev[key] = row["price"]

    return alerts