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

    def _test_init(self):
        v_info = self.monitoring.DataSource.init({'options': {}})
        print_json(v_info)

    def _test_verify(self):
        options = {
        }
        v_info = self.monitoring.DataSource.verify({'options': options, 'secret_data': self.appd_credentials})
        print_json(v_info)

    def test_metric_list(self):
        query = {
            "metric_list": "/controller/rest/applications/439/metrics?metric-path=Overall%20Application%20Performance"
        }
        options = {}
        resource = self.monitoring.Metric.list({'secret_data': self.appd_credentials,
                                                'options': options, 
                                                            'query': query})

        print_json(resource)


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
