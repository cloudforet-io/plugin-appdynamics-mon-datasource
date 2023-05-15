import logging
from spaceone.core.service import *
from spaceone.monitoring.manager.appdynamics_manager import AppdynamicsManager
from spaceone.monitoring.manager.data_source_manager import DataSourceManager

_LOGGER = logging.getLogger(__name__)
DEFAULT_SCHEMA = 'appdynamics_client_secret'

@authentication_handler
@authorization_handler
@event_handler
class DataSourceService(BaseService):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @check_required(['options'])
    def init(self, params):
        """ init plugin by options
        """
        self.data_source_mgr: DataSourceManager = self.locator.get_manager('DataSourceManager')
        return self.data_source_mgr.init_response()

    @transaction
    @check_required(['options', 'secret_data'])
    def verify(self, params):
        """ Verifying data source plugin

        Args:
            params (dict): {
                'schema': 'str',
                'options': 'dict',
                'secret_data': 'dict'
            }

        Returns:
            plugin_verify_response (dict)
        """
        self.appdynamics_mgr: AppdynamicsManager = self.locator.get_manager('AppdynamicsManager')
        self.appdynamics_mgr.verify(params.get('schema', DEFAULT_SCHEMA), params['options'], params['secret_data'])
