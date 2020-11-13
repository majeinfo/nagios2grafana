import re
from host_service_status import HostStatus, ServiceStatus

# TODO: convert types

class NagiosFileReader:
    re_host_status = re.compile('^hoststatus[ ]+{')
    re_svc_status = re.compile('^servicestatus[ ]+{')
    re_host_name = re.compile('^[ \t]*host_name=(.*)')
    re_check_execution_time = re.compile('^[ \t]*check_execution_time=(.*)')
    re_current_state = re.compile('^[ \t]*current_state=(.*)')
    re_plugin_output = re.compile('^[ \t]*plugin_output=(.*)')
    re_last_check = re.compile('^[ \t]*last_check=(.*)')
    re_service_description = re.compile('^[ \t]*service_description=(.*)')
    re_end_status = re.compile('^[ \t]*}')

    host_attrs = {
        'host_name': re_host_name,
        'check_execution_time': re_check_execution_time,
        'current_state': re_current_state,
        'plugin_output': re_plugin_output,
        'last_check': re_last_check,
    }

    svc_attrs = {
        'host_name': re_host_name,
        'service_description': re_service_description,
        'check_execution_time': re_check_execution_time,
        'current_state': re_current_state,
        'plugin_output': re_plugin_output,
        'last_check': re_last_check,
    }

    def __init__(self, filename):
        self._nagios_filename = filename
        try:
            with open(filename):
                pass
        except Exception as e:
            print(f"File {filename} could not be opened")
            raise e

    def read_status(self):
        host_status = []
        svc_status = []

        try:
            with open(self._nagios_filename) as f:
                try:
                    for line in f:
                        if NagiosFileReader.re_host_status.match(line):
                            host_status.append(self._get_host_status(f))
                            continue
                        if NagiosFileReader.re_svc_status.match(line):
                            svc_status.append(self._get_svc_status(f))
                            continue
                except Exception as e:
                    print(e)
        except Exception as e:
            print(f"File {self._nagios_filename} could not be opened")
            print(e)

        return host_status, svc_status

    def _get_host_status(self, f):
        h = {}
        for line in f:
            for attr, regex in NagiosFileReader.host_attrs.items():
                mobj = regex.match(line)
                if mobj:
                    if regex.groups > 0:
                        h[attr] = mobj.group(1)
                    continue

            if NagiosFileReader.re_end_status.match(line):
                break

        return HostStatus(**h)

    def _get_svc_status(self, f):
        s = {}
        for line in f:
            for attr, regex in NagiosFileReader.svc_attrs.items():
                mobj = regex.match(line)
                if mobj:
                    if regex.groups > 0:
                        s[attr] = mobj.group(1)
                    continue

            if NagiosFileReader.re_end_status.match(line):
                break

        return ServiceStatus(**s)

