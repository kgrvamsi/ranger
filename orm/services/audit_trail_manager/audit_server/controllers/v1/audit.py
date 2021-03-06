"""audit controller module."""

from orm.services.audit_trail_manager.audit_server.controllers.v1 import configuration, logs, transaction


class AuditController(object):
    """audit controller."""

    transaction = transaction.TransactionController()
    logs = logs.LogsController()
    configuration = configuration.ConfigurationController()
