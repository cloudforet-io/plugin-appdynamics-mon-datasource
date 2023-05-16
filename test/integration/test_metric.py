import os
import unittest
import json

from spaceone.core.unittest.result import print_data
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import config
from spaceone.core import utils
from spaceone.core.transaction import Transaction
from spaceone.tester import TestCase, print_json


class TestCollector(TestCase):

    @classmethod
    def setUpClass(cls):
        appd_cred = os.environ.get('APPD_CRED')
        test_config = utils.load_yaml_from_file(appd_cred)

        cls.schema = 'appdynamics_client_secret'
        cls.appd_credentials = test_config
        super().setUpClass()

    def test_init(self):
        v_info = self.monitoring.DataSource.init({'options': {}})
        print_json(v_info)

    def test_verify(self):
        options = {
        }
        v_info = self.monitoring.DataSource.verify({'options': options, 'secret_data': self.appd_credentials})
        print_json(v_info)

    def test_metric_list(self):
        query = {
            "path": "/controller/rest/applications/439/metrics",
            "params": {"metric-path": "Overall Application Performance"},
            "data": "/controller/rest/applications/439/metric-data",
        }
        options = {}
        resource = self.monitoring.Metric.list({'secret_data': self.appd_credentials,
                                                'options': options, 
                                                            'query': query})

        print_json(resource)

    def test_metric_get_data(self):
        query = {
            "cloud-svc-ef1d1a49038c": {
                "path": "/controller/rest/applications/439/metric-data",
                "params": {"metric-path": "Overall Application Performance|Calls per Minute"}
                }
        }
        options = {}
        resource = self.monitoring.Metric.get_data({'secret_data': self.appd_credentials,
                                                'options': options, 
                                                'metric': 'Calls per Minute',
                                                'stat': 'AVERAGE',
                                                "start": "2023-05-08T09:23:22.417Z",
                                                "end": "2023-05-09T09:23:22.417Z", 
                                                'metric_query': query})
        print_json(resource)


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
