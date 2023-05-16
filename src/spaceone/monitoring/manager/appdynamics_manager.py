import logging
import time
import datetime

from spaceone.core.manager import BaseManager
from spaceone.monitoring.error import *
from spaceone.monitoring.connector.metric import MetricConnector
from spaceone.monitoring.libs.connector import AppdynamicsConnector

_LOGGER = logging.getLogger(__name__)

_STAT_MAP = {
    'AVERAGE': 'value',
    'MAX': 'max',
    'MIN': 'min',
    'SUM': 'sum'
}


class AppdynamicsManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.appdynamics_connector: AppdynamicsConnector = self.locator.get_connector('AppdynamicsConnector')

    def verify(self, schema, options, secret_data):
        """ Check connection
        """
        self.appdynamics_connector.set_connect(secret_data)

    def set_connector(self, schema, secret_data):
        self.appdynamics_connector.set_connect(secret_data)

    def list_metrics(self, schema, options, secret_data, query):
        self.metric_connector: MetricConnector = self.locator.get_connector('MetricConnector')

        metrics_info = []

        self.metric_connector.set_connect(secret_data)

        data_path = query.get('data', None)
        metric_path = self._get_metric_path(query.get('params', {}))

        for metric in self.metric_connector.list_metrics(query):
            if metric.get("type", None) != "leaf":
                continue
            name = metric.get("name", None)
            # TODO: check name
            _metric = {
                'key': name,
                'name': name,
                'metric_query': {       # metric_query is used for get_metric_data
                    'path': data_path,
                    'params': {
                        'metric-path': f"{metric_path}|{name}"
                    }
                }
            }

            metrics_info.append(_metric)

        return {'metrics': metrics_info}

    def get_metric_data(self, schema, options, secret_data, metric_query, metric, start, end, period, stat):
        self.metric_connector: MetricConnector = self.locator.get_connector('MetricConnector')
        self.metric_connector.set_connect(secret_data)

        get_data_set = {
            'labels': [],
            'values': {}
        }

        time_param = self._update_time(start, end, period)
        for cloud_service_id, _metric in metric_query.items():
            query = _metric
            params = query.get('params', {})
            # Add Timestamp
            params.update(time_param)
            # Add rollup
            params.update({'rollup': 'false'})
            query['params'] = params
            response = self.metric_connector.get_metric_data(query)
            labels, values = self._parse_response(response, stat)

            if not get_data_set.get('labels') and len(labels) > 0:
                get_data_set['labels'] = labels

            get_data_set['values'].update({cloud_service_id: values})

        return get_data_set

    @staticmethod
    def _get_metric_path(params):
        item = params.get('metric-path', None)
        return item

    @staticmethod
    def _update_time(start, end, period):
        # TODO: support period
        time_param = {
            'start-time': int(start.timestamp() * 1000),
            'end-time': int(end.timestamp() * 1000),
            'time-range-type': 'BETWEEN_TIMES',
        }

        return time_param


    @staticmethod
    def _parse_response(results, stat):
        """ loop the result
        labels:
            - '2023-05-15T23:25:00.000Z'
            - '2023-05-16T00:25:00.000Z'
            - '2023-05-16T01:25:00.000Z'
            - '2023-05-16T02:25:00.000Z'
            - '2023-05-16T03:25:00.000Z'
            - '2023-05-16T04:25:00.000Z'
            - '2023-05-16T05:25:00.000Z'
        values:
            - 1.8815680988278385
            - 0.47066669718563786
            - 0.4779445720623954
            - 0.4732778952037731
            - 0.47961111288213926
            - 0.4701945271923452
            - 0.724423300848668
        """
        labels = []
        values = []
        # len of results == 1
        if len(results) == 0:
            return labels, values

        result = results[0]
        items = result.get('metricValues', [])
        for item in items:
            timestamp = item.get('startTimeInMillis', None) / 1000
            dt = datetime.datetime.fromtimestamp(timestamp)
            labels.append(dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
            value = item.get(_STAT_MAP[stat], None)
            values.append(value)

        print(labels)
        print(values)
        return labels, values
