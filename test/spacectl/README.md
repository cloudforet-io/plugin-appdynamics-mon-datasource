# Register Plugin


# Register DataSource

filename: register_mon.yaml

~~~
---
name: appdynamics
plugin_info:
  plugin_id: plugin-appdynamics-mon-datasource
  provider: appdynamics
~~~

Command

~~~
spacectl exec register monitoring.DataSource -f register_mon.yaml
~~~

