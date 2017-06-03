from ims.ims_mocks import requests_mock
from ims.ims_mocks import audit_mock

from ims.persistency.sql_alchemy.data_manager import DataManager
from ims.logic import image_logic
from ims.logic import metadata_logic
from ims.proxies import rds_proxy
from orm_common.utils import utils

providers = [
    ('rds_proxy', rds_proxy),
    ('image_logic', image_logic),
    ('metadata_logic', metadata_logic),
    ('requests', requests_mock),
    ('data_manager', DataManager),
    ('utils', utils),
    ('audit_client', audit_mock)
]