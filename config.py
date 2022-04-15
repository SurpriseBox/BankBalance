
from kombu import Queue


class Config:
    """
    Overall service config.
    """
    DB_URL = 'mysql+aiomysql://root:p#ssw0rd1@mysqldb/bank_balance'

    class CeleryConfig:
        """
        Celery config.
        """
        broker_url = f"amqp://guest:guest@rabbitmq:5672//"
        task_queues = (
            Queue('created_operations', routing_key='operation.created'),
            Queue('pending_operations', routing_key='operation.pending'),
        )
        imports = [
            'apps.operations.celery_tasks',
            'apps.users.celery_tasks'
        ]
        task_routes = {
            'operations.begin_process_operation': {
                'queue': 'created_operations',
                'routing_key': 'operation.created'
            },
            'operations.process_operation': {
                'queue': 'pending_operations',
                'routing_key': 'operation.pending'
            }
        }
