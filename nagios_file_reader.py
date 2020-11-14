import re

class NagiosFileReader:
    re_host_status = re.compile('^hoststatus[ ]+{')
    re_svc_status = re.compile('^servicestatus[ ]+{')
    re_host_name = re.compile('^[ \t]*host_name=(.*)')
    #re_check_execution_time = re.compile('^[ \t]*check_execution_time=(.*)')
    re_current_state = re.compile('^[ \t]*current_state=(.*)')
    re_plugin_output = re.compile('^[ \t]*plugin_output=(.*)')
    re_last_check = re.compile('^[ \t]*last_check=(.*)')
    re_service_description = re.compile('^[ \t]*service_description=(.*)')
    re_end_status = re.compile('^[ \t]*}')

    host_attrs = {
        'current_state': re_current_state,
        'host_name': re_host_name,
        #'check_execution_time': re_check_execution_time,
        'last_check': re_last_check,
        'plugin_output': re_plugin_output,
    }

    svc_attrs = {
        'current_state': re_current_state,
        'host_name': re_host_name,
        'service_description': re_service_description,
        #'check_execution_time': re_check_execution_time,
        'last_check': re_last_check,
        'plugin_output': re_plugin_output,
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
                            host_status.append(self._get_status(f, NagiosFileReader.host_attrs))
                            continue
                        if NagiosFileReader.re_svc_status.match(line):
                            svc_status.append(self._get_status(f, NagiosFileReader.svc_attrs))
                            continue
                except Exception as e:
                    print(e)
        except Exception as e:
            print(f"File {self._nagios_filename} could not be opened")
            print(e)

        return host_status, svc_status

    def _get_status(selfself, f, attrs):
        d = {}
        for line in f:
            for attr, regex in attrs.items():
                mobj = regex.match(line)
                if mobj:
                    if regex.groups > 0:
                        d[attr] = mobj.group(1)
                        if attr == 'last_check':
                            # Convert second to milliseconds
                            d[attr] = int(d[attr]) * 1000
                    continue

            if NagiosFileReader.re_end_status.match(line):
                break

        return d

