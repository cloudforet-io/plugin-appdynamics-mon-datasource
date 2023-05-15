import logging
import requests

from spaceone.monitoring.libs.connector import AppdynamicsConnector
from spaceone.monitoring.error.appdynamics import *
__all__ = ['MetricConnector']
_LOGGER = logging.getLogger(__name__)


class MetricConnector(AppdynamicsConnector):
    """
    https://docs.appdynamics.com/appd/22.x/22.3/en/extend-appdynamics/appdynamics-apis/application-model-api
    
    * Metrics
    * Business Transaction
    * Tiers
    * Registered Backends
    * Node Information
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_connect(kwargs.get('secret_data'))

    def list_all_applications(self):
        # GET /controller/rest/applications
        PATH = "/controller/rest/applications"
        return self.make_request(PATH)
