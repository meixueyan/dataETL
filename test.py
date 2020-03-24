from flaskr.app import app
from flask import Flask, request
from flask_apscheduler import APScheduler
import datetime


class Config(object):
    JOBS = [
        {
            'id': 'job',
            'func': '__main__:method_test',
            'args': None,
            'trigger': 'interval',
            'seconds': 10
        },
        {
            'id': 'job2',
            'func': '__main__:method_test_cron',
            'args': None,
            'trigger': 'cron',
            'day_of_week':"mon-sun",
            'hour':'23',
            'minute':'55'
        }
    ]

    SCHEDULER_API_ENABLED = True


def method_test():
    print("The binary is runnung at:%s" % (datetime.datetime.now()))


def method_test_cron():
    print("The cron is runnung at:%s" % (datetime.datetime.now()))


app.config.from_object(Config())

if __name__ == "__main__":
    scheduler=APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    app.run(debug=False)



# from crontab import CronTab

# cron = CronTab(user=)

# job = cron.new(command='/Users/xueyanmei/development/dataETL/venv/bin/python3.7 ./flaskr/app.py', comment='comment')
# job.minute.every(1)

# job.clear()

# cron.write()
