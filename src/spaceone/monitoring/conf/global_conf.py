CONNECTORS = {
    'AppdynamicsConnector': {
        'backend': 'spaceone.monitoring.libs.connector.AppdynamicsConnector',
    },
    'MetricConnector': {}
}

LOG = {
    'filters': {
        'masking': {
            'rules': {
                'DataSource.verify': [
                    'secret_data'
                ],
                'Metric.list': [
                    'secret_data'
                ],
                'Metric.get_data': [
                    'secret_data'
                ],
                'Log.list': [
                    'secret_data'
                ],
            }
        }
    }
}
