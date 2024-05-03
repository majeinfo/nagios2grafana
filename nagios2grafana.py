"""
This is simple Bridge that reads a Nagios Status file and transform it into JSON documents
so it can be exposed to the Grafana JSON Datasource Plugin.
It allows you to create a Dashboard that would include a Panel of type Table containing
the last Hosts and Service statuses reported by Nagios.
This Bridge also supports filtering : the filters are given as JSON document in the Grafana Query Panel.
"""
import argparse
import threading
import time
import atexit
import logging
import traceback
import sys
import os
from flask import Flask, json, request
import nagios_file_reader as nfr
import status_exporter as exp

args = None
api = None

def main():
    global args, api
    parser = argparse.ArgumentParser(description='Bridge from nagios status.dat to Grafana dashboard')
    parser.add_argument('-v', '--verbosity', action='store_true',
                        help='increase output verbosity')
    parser.add_argument('-i', '--interval', type=int, dest='interval', default=30,
                        help='nagios status file analysis interval (in seconds)')
    parser.add_argument('-p', '--port', type=int, dest='listen_port', default=5000,
                        help='listening port')
    parser.add_argument('--nagios-status-file', dest='nagios_status_file', required=True,
                        help='path to nagios status file')
    args = parser.parse_args()

    log_level = logging.ERROR
    if 'DEBUG' in os.environ or args.verbosity:
        log_level = logging.DEBUG

    logging.basicConfig(level=log_level)

    reader = nfr.NagiosFileReader(args.nagios_status_file)

    # Init
    host_status, svc_status = reader.read_status()

    # Create and start the background Thread that will read the Nagios status file
    data_lock = threading.Lock()

    def thread_function():
        while True:
            with data_lock:
                host_status, svc_status = reader.read_status()

            time.sleep(args.interval)

    thread = threading.Thread(target=thread_function)
    thread.daemon = True
    thread.start()

    # Create the Web Server and handle the requests
    api = Flask(__name__)

    @api.route('/', methods=['GET'])
    def home():
        return json.dumps({"status": "OK"})

    @api.route('/search', methods=['POST'])
    @api.route('/metrics', methods=['POST'])
    def search():
        logging.debug("/search or /metrics")
        metrics = ["nagios_host_status", "nagios_service_status"]
        return json.dumps(metrics)

    @api.route('/query', methods=['POST'])
    def query():
        req = request.get_json()
        logging.debug(f'/query {req}')
        results = {}
        with data_lock:
            try:
                #type = req['targets'][0]['type']
                type = "table"
                target = req['targets'][0]['target']
                logging.debug(f'type={type}, target={target}')

                if type == "table":
                    if target == 'nagios_host_status':
                        results = exp.build_host_data(req['targets'][0], host_status)
                    elif target == 'nagios_service_status':
                        results = exp.build_svc_data(req['targets'][0], svc_status)
                    else:
                        results = {'msg': f'target {target} not supported'}
                else:
                    results = {'msg': f'type {type} not supported'}
            except Exception as e:
                traceback.print_exc()
                logging.error(e)

        logging.debug(f"{results}")
        return json.dumps(results)

    return api


# Gunicorn entry point generator
# To be run like this :
# $ gunicorn -b IP:port 'nagios2grafana:app(nagios_status_file="/path/to/status/fat")' -D
def app(*args, **kwargs):
    sys.argv = [sys.argv[0]]
    for k in kwargs:
        k2 = k.replace('_', '-')
        sys.argv.append("--" + k2)
        sys.argv.append(kwargs[k])

    return main()

if __name__ == '__main__':
    main()
    api.run(port=args.listen_port, debug=False)


