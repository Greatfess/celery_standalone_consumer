import time

from celery import Celery
from celery.utils.log import get_task_logger
from kombu.serialization import register


log1 = get_task_logger(__name__)
app = Celery()
app.config_from_object('celeryconfig')


@app.task(name='foo.add')
def add(x, y):
    log1.info ('Adding %.2f and %.2f' %(x,y))
    # calculate and return 
    return x + y


@app.task(name='foo.adda')
def adda(*args):
    '''A simple task adding all arguments'''
    log1.info(f'Adding numbers {repr(args)}')
    return sum(args)


@app.task(name='foo.addi')
def addi(it):
    '''A simple task adding all items from iterable'''
    log1.info(f'Adding numbers {repr(it)}')
    return sum(it)


@app.task(name='foo.mul')
def mul(x, y):
    log1.info('Multiplying %.2f and %.2f' %(x,y))
    return x * y


@app.task(name='foo.waste_time')
def waste_time(n=12, callback=None): 
    for i in range(n):
        log1.info('Wasting some time (%d/%d)' % (i, n))
        time.sleep(5)
    if callback:
        log1.info('Finished task: About to invoke %r' % (callback))
        app.subtask(callback).delay()
    else:
        log1.info('Finished task')
    return {'status': 'wasted'}


if __name__ == "__main__":
    worker = app.Worker(
        # include=['sample_service'],
        loglevel='INFO'
    )
    worker.start()

    # It's better to use this command:
    # celery -A sample_service worker -l INFO -n sample_service@%h --autoscale=10,3
    # -A sample_service - name of the module with tasks,
    # -n sample_service@%h - worker name (for flower)   %h - node name
    # --autoscale=10,3 - max,min workers count
