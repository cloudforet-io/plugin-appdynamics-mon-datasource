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
        #self.set_connect(kwargs.get('secret_data'))

    def list_metrics(self, query):
        """
        query: {
            "path": "/controller/rest/applications/{application_id}/metrics"
            "params": {
                "metric-path": "Overall Application Performance"
            }
        }
        """
        # GET /controller/rest/applications
        path = query.get("path", None)
        if path is None:
            print(query)
            # TODO: raise ERROR_REQUIRED_PARAMETER(key="path")
        params = query.get("params", None)
        return self.make_request(path, params)


    def get_metric_data(self, query):
        """
        query: {
            "path": "/controller/rest/applications/{application_id}/metric-data"
            "params": {
                "metric-path": "Overall Application Performance%7CCalls per Minute",
                "start-time": "",
                "end-time": "",
                "rollup": "false",
            }
        }
        """
        # GET /controller/rest/applications
        path = query.get("path", None)
        if path is None:
            print(query)
            # TODO: raise ERROR_REQUIRED_PARAMETER(key="path")
        params = query.get("params", None)
        return self.make_request(path, params)
