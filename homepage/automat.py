from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from homepage import run_webscraper

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_webscraper.save_data_from_scrapers(), 'interval', minutes=30)
    scheduler.start()