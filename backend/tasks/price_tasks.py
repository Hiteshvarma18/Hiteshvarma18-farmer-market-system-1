from celery_config import celery
from services.live_price_service import (
    update_prices_from_csv
)

@celery.task
def refresh_prices():

    rows = update_prices_from_csv(
        "data/mandi.csv"
    )

    return {
        "rows_imported": rows
    }