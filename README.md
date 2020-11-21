This a small Python program that acts as a bridge between *Nagios* and *Grafana* :

it reads the *Nagios* Status file and exposes the Hosts and Services last checks
as JSON documents for the *Grafana* JSON-Datasource Plugin.

You can then create a Dashboard for *Grafana* that contains one or more Panels
with the Hosts or the Services statuses !

*nagios2grafana* can be run using *gunicorn* like this :

```
$ gunicorn -b IP:port 'nagios2grafana:app(nagios_status_file="/path/to/status.dat")'
```

But you can also run it from a Container image :

```
$ docker container run -d -v /path/to/your/status.dat:/app/status.dat \
                          -p 5000:5000 majetraining/nagios2grafana
```

The *Grafana Query Panel* allows you to filter the data that will be displayed.
You can define filters using regexp enclosed between slashes.

Some filter examples:

```
{"host_name": "only_one_server"}
{"service_description": "check web", "current_state": "2"}	(only critical services)
{"host_name": "/web/"}		(only servers which name matches "web" re)
```
