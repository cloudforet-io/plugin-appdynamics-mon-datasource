# Prerequisite

To test appdynamics plugin, you need api credentials

save api credentials in your local disk

For example, put on ~/.secret/appd.yaml

The credentials contents

~~~
---
client_name=<client_name>
account_name=<account_name>
client_secret=<client_secret>
controller=<Controller URL>
~~~

Configure as your environment

~~~
export APPD_CRED=~/.secret/appd.yaml
~~~

# Test

~~~
spaceone test -c config.yaml -s scenario.json
~~~ 
