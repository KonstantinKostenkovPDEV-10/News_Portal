from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler


def schedule_api():
    print('hello')
def start():
	scheduler = BackgroundScheduler()
	scheduler.add_job(schedule_api, 'interval', seconds=5)
	scheduler.start()