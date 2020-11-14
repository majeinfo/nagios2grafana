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
    for h in host_status:
        if _filtered(req_data, h):
            host_data[0]['rows'].append(
                [h['current_state'], h['host_name'], h['last_check'], '> ' + h['plugin_output']]
        )

    return host_data


def build_svc_data(req_data, svc_status):
    svc_data[0]['rows'] = []
    for s in svc_status:
        if _filtered(req_data, s):
            svc_data[0]['rows'].append(
                [s['current_state'], s['host_name'], s['service_description'], s['last_check'], '> ' + s['plugin_output']]
            )

    return svc_data

def _filtered(req, data):
    if 'data' not in req or type(req['data']) != dict:
        return True

    for d in data:
        for attr, value in req['data'].items():
            if attr in d:
                if d[attr] != value:
                    break
        else:
            return True

    return False

