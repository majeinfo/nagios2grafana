This a small Python program that acts as a bridge between Nagios and Grafana :

it reads the Nagios Status file and expose the host and service last checks
as JSON documents for the Grafana JSON Datasource Plugin.

You can then create a Dashboard for Grafana that contains one or more Panels
with the Hosts or the Services statuses !

The Grafanq Query Panel allows you to filter the data that would be displayed.
