from schematics import Model
from schematics.types import BaseType, ListType, DictType, StringType
from schematics.types.compound import ModelType

__all__ = ['MetricsModel']


class MetricModel(Model):
    key = StringType(required=True)
    name = StringType(required=True)
    unit = DictType(BaseType, serialize_when_none=False )
    group = StringType(serialize_when_none=False)
    metric_query = DictType(BaseType, default={})


class MetricsModel(Model):
    metrics = ListType(ModelType(MetricModel), required=True)

