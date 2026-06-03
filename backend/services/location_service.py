from db import get_db

def get_markets():

    db = get_db()

    cursor = db.cursor(
        dictionary=True
    )

    cursor.execute("""
    SELECT DISTINCT market
    FROM crop_prices
    ORDER BY market
    """)

    markets = cursor.fetchall()

    cursor.close()
    db.close()

    return markets


def get_market_prices(market):

    db = get_db()

    cursor = db.cursor(
        dictionary=True
    )

    cursor.execute("""
    SELECT
        crop,
        market,
        price,
        date
    FROM crop_prices
    WHERE market=%s
    ORDER BY date DESC
    """, (market,))

    rows = cursor.fetchall()

    cursor.close()
    db.close()

    return rows