This a small Python program that acts as a bridge between *Nagios* and *Grafana* :

it reads the *Nagios* Status file and exposes the Hosts and Services last checks
as JSON documents for the *Grafana* JSON-Datasource Plugin.

You can then create a Dashboard for *Grafana* that contains one or more Panels
with the Hosts or the Services statuses !

*nagios2grafana* can be run using *gunicorn* like this :

```
$ gunicorn -b IP:port 'nagios2grafana:app(nagios_status_file="/path/to/status.dat")'
```

The *Grafana Query Panel* allows you to filter the data that would be displayed.
