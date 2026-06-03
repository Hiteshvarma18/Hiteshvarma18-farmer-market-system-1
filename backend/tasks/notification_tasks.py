from celery_config import celery
from services.price_alert_service import detect_price_alerts
from services.notification_service import send_sms

@celery.task
def run_price_alerts():

    alerts = detect_price_alerts()

    sent = 0

    # DEMO: single number (upgrade later to user table)
    demo_phone = "9999999999"

    for alert in alerts:

        send_sms(demo_phone, alert["message"])
        sent += 1

    return {
        "alerts_generated": len(alerts),
        "alerts_sent": sent
    }