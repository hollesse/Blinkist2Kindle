from apscheduler.schedulers.blocking import BlockingScheduler

from main import cronjob

scheduler = BlockingScheduler()
#scheduler.add_job(cronjob, 'cron', hour=0, minute=00)
scheduler.add_job(cronjob, 'interval', seconds=30)

scheduler.start()
