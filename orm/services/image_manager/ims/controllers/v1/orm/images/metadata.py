from orm.common.orm_common.injector import injector
from orm.common.orm_common.utils import api_error_utils as err_utils
from orm.services.image_manager.ims.logger import get_logger
from orm.services.image_manager.ims.logic.error_base import ErrorStatus
from orm.services.image_manager.ims.persistency.wsme.models import MetadataWrapper
from orm.services.image_manager.ims.utils import authentication as auth

from pecan import request, rest
from wsmeext.pecan import wsexpose

LOG = get_logger(__name__)

di = injector.get_di()


@di.dependsOn('metadata_logic')
@di.dependsOn('utils')
class MetadataController(rest.RestController):
    @wsexpose(str, str, str, body=MetadataWrapper, rest_content_types='json', status_code=200)
    def post(self, image_id, region_name, metadata_wrapper):  # add metadata to region
        metadata_logic, utils = di.resolver.unpack(MetadataController)
        auth.authorize(request, "metadata:create")

        try:
            LOG.info("MetadataController - add metadata: " + str(metadata_wrapper))

            metadata_logic.add_metadata(image_id, region_name, metadata_wrapper)

            LOG.info("MetadataController - metadata added")
            return "OK"

        except ErrorStatus as exception:
            LOG.log_exception("MetadataController - Failed to add metadata", exception)
            raise err_utils.get_error(request.transaction_id,
                                      message=exception.message,
                                      status_code=exception.status_code)
        except Exception as exception:
            LOG.log_exception("MetadataController - Failed to add metadata", exception)
            raise err_utils.get_error(request.transaction_id,
                                      status_code=500,
                                      error_details=exception.message)
