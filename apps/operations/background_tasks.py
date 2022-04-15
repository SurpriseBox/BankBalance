
from apps.operations.celery_tasks import process_operation, begin_process_operation
from db.models import Operation


def add_operation_to_query(operation: Operation):
    begin_process_operation.apply_async(args=[operation.id], link=process_operation.s())
