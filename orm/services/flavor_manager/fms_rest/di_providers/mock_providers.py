from fms_mocks import audit_mock, requests_mock
from fms_rest.data.sql_alchemy.data_manager import DataManager
from fms_rest.logic import flavor_logic
from fms_rest.proxies import rds_proxy
from fms_rest.utils import utils

providers = [
    ('rds_proxy', rds_proxy),
    ('flavor_logic', flavor_logic),
    ('requests', requests_mock),
    ('data_manager', DataManager),
    ('utils', utils),
    ('audit_client', audit_mock)
]
