from kombu import Exchange, Queue


## Broker settings.
broker_url = 'pyamqp://guest:guest@127.0.0.1:5672'

# ack после выполнения таска
task_acks_late = True
# Even if task_acks_late is enabled, the worker will acknowledge tasks
# when the worker process executing them abruptly exits or is signaled (e.g., KILL/INT, etc).
# Setting this to true allows the message to be re-queued instead,
# so that the task will execute again by the same worker, or another worker
task_reject_on_worker_lost = True

worker_prefetch_multiplier = 1

## Using the database to store task state and results.
# result_backend = 'amqp'
result_backend = "rpc"
# Если не нужно отправлять ответ 
# task_ignore_result = True

result_backend_always_retry = True
result_backend_max_sleep_between_retries_ms = 10000
task_serializer = 'json'
result_serializer = "json"
# result_compression = "gzip"

task_annotations = {'tasks.add': {'rate_limit': '10/s'}}

accept_content = ['application/json', 'application/data']
result_accept_content = ['application/json', 'application/data']
task_default_queue = 'project.env.default'

worker_log_format = '[%(asctime)s: %(processName)s:%(filename)s:%(funcName)s:%(lineno)d:%(levelname)s] - %(message)s'
worker_task_log_format = '[%(asctime)s: %(processName)s:%(task_name)s:%(filename)s:%(funcName)s:%(lineno)d:%(levelname)s] - %(message)s'

# 1. Messages are sent to exchanges.
# 2. An exchange routes messages to one or more queues. Several exchange types exists, 
#    providing different ways to do routing, or implementing different messaging scenarios.
# 3. The message waits in the queue until someone consumes it.
# 4. The message is deleted from the queue when it has been acknowledged.

# The steps required to send and receive messages are:
# 1. Create an exchange
# 2. Create a queue
# 3. Bind the queue to the exchange.

# Celery automatically creates the entities necessary for the queues in task_queues to work 
# (except if the queue’s auto_declare setting is set to False).
# Here’s an example queue configuration with five queues;
task_queues = (
    Queue('foo.add', Exchange('celery_reports'), routing_key='foo.add'),
    Queue('foo.adda',  Exchange('celery_reports'),   routing_key='foo.adda'),
    Queue('foo.addi',  Exchange('celery_reports'),   routing_key='foo.addi'),
    Queue('foo.mul', Exchange('celery_reports2'), routing_key='foo.mul'),
    Queue('foo.waste_time', Exchange('celery_reports2'), routing_key='foo.waste_time'),
)
task_default_queue = 'celery_default'
task_default_exchange_type = 'direct'
task_default_routing_key = 'celery_default'

# For flower
worker_send_task_events = True

# task_routes = ([
#     ('import_feed', {'queue': 'queue_import_feed'})
# ])

