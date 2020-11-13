host_data = [{
    "type": "table",
    "columns": [
        {"text": "host name", "type": "string"},
        {"text": "check_execution_time", "type": "number"},
        {"text": "current_state", "type": "number"},
        {"text": "plugin_output", "type": "string"},
        {"text": "last_check", "type": "number"},
    ],
    "rows": [
        #['webserver', 'OK', 0],
        #['dbserver', 'Warning', 1],
    ]
}]

svc_data = [{
    "type": "table",
    "columns": [
        {"text": "host name", "type": "string"},
        {"text": "service description", "type": "string"},
        {"text": "check_execution_time", "type": "number"},
        {"text": "current_state", "type": "number"},
        {"text": "plugin_output", "type": "string"},
        {"text": "last_check", "type": "number"},
    ],
    "rows": [
        #['webserver', 'Apache', 'OK', 0],
        #['webserver', 'Disk', 'OK', 0],
        #['dbserver', 'Mongod process', 'Warning', 1],
    ]
}]

def build_host_data(host_status):
    host_data[0]['rows'] = []

    for h in host_status:
        host_data[0]['rows'].append(
            [h.host_name, h.check_execution_time, h.current_state, h.plugin_output, h.last_check]
        )

    return host_data


def build_svc_data(svc_status):
    svc_data[0]['rows'] = []

    for s in svc_status:
        svc_data[0]['rows'].append(
            [s.host_name, s.service_description, s.check_execution_time, s.current_state, s.plugin_output, s.last_check]
        )

    return svc_data
