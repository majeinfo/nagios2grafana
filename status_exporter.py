host_data = [{
    "type": "table",
    "columns": [
        {"text": "Current State", "type": "number"},
        {"text": "Hostname", "type": "string"},
        #{"text": "check_execution_time", "type": "number"},
        {"text": "last_check", "type": "time"},
        {"text": "plugin_output", "type": "string"},
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
        {"text": "last_check", "type": "time"},
        {"text": "plugin_output", "type": "string"},
    ],
    "rows": []
}]

# Make sure the plugin_output does not start with a number (Grafana bug ?)
def build_host_data(host_status):
    host_data[0]['rows'] = []
    for h in host_status:
        host_data[0]['rows'].append(
            [h['current_state'], h['host_name'], h['last_check'], '> ' + h['plugin_output']]
        )

    return host_data


def build_svc_data(svc_status):
    svc_data[0]['rows'] = []
    for s in svc_status:
        svc_data[0]['rows'].append(
            [s['current_state'], s['host_name'], s['service_description'], s['last_check'], '> ' + s['plugin_output']]
        )

    return svc_data
