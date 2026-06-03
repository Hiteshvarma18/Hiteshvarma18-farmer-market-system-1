import schedule
import time
import requests

def job():

    requests.get("http://127.0.0.1:8000/api/live/run-alerts")

    print("Smart alerts triggered")

schedule.every().day.at("07:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)