"""
Code for functions that build the JSON result for the /query request
sent by Grafana JSON Datasource Plugin.
We prefer the lazy model : results are computed for each request and not
when the Nagios status file is read. This makes the filtering process easier.
"""
import re
import logging


host_data = [{
    "type": "table",
    "columns": [
        {"text": "Current State", "type": "number"},
        {"text": "Hostname", "type": "string"},
        #{"text": "check_execution_time", "type": "number"},
        {"text": "Last Check", "type": "time"},
        {"text": "Plugin Output", "type": "string"},
    ],
    "rows": []
}]


svc_data = [{
    "type": "table",
    "columns": [
        {"text": "Current State", "type": "number"},
        {"text": "Hostname", "type": "string"},
        {"text": "Service Description", "type": "string"},
        #{"text": "check_execution_time", "type": "number"},
        {"text": "Last Check", "type": "time"},
        {"text": "Plugin Output", "type": "string"},
    ],
    "rows": []
}]


# Make sure the plugin_output does not start with a number (Grafana bug ?)
def build_host_data(req_data, host_status):
    host_data[0]['rows'] = []
    _compile_re(req_data)
    logging.debug(f"filters: {req_data['filters']}")
    for h in host_status:
        if _filtered(req_data, h):
            host_data[0]['rows'].append(
                [h['current_state'], h['host_name'], h['last_check'], '> ' + h['plugin_output']]
        )

    return host_data


def build_svc_data(req_data, svc_status):
    svc_data[0]['rows'] = []
    _compile_re(req_data)
    logging.debug(f"filters: {req_data['filters']}")
    for s in svc_status:
        if _filtered(req_data, s):
            svc_data[0]['rows'].append(
                [s['current_state'], s['host_name'], s['service_description'], s['last_check'], '> ' + s['plugin_output']]
            )

    return svc_data


# Grafana may use 'data' or 'payload' key, depending of its version
def _compile_re(req):
    logging.debug(f"_compile_re: {req}")
    req['filters'] = {}

    if 'data' in req:
        if type(req['data']) != dict:
            return 

        filter_field = 'data'
    elif 'payload' in req:
        if type(req['payload']) != dict:
            return

        filter_field = 'payload'
    else:
        return


    for attr, value in req[filter_field].items():
        if value[0] == '/' and value[-1] == '/':
            req['filters'][attr] = re.compile(value[1:-1])
        else:
            req['filters'][attr] = value


def _filtered(req, data):
    for attr, value in req['filters'].items():
        if attr in data:
            #if type(value) == re.Pattern:  (not supported before python3.7)
            if type(value) != str:
                if value.search(data[attr]) is None:
                    break
            elif data[attr] != value:
                break
    else:
        return True

    return False

