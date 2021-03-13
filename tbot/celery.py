from celery import Celery


app = Celery('Exchange',
             backend='redis://default:redis_pass_@redis:6379/0',
             broker='redis://default:redis_pass_@redis:6379/0',
             include=['tbot.tasks'])

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json'
)

app.conf.beat_schedule = {
    'every-second': {
        'task': 'tbot.tasks.main_currency',
        'schedule': 1.0,
        'args': (),
    },
}

