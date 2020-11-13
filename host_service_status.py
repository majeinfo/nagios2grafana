class HostStatus:
    __slots__ = ('host_name', 'check_execution_time', 'current_state', 'plugin_output', 'last_check')

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)


class ServiceStatus:
    __slots__ = ('host_name', 'service_description', 'check_execution_time', 'current_state', 'plugin_output', 'last_check')

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)

