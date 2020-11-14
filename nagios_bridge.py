"""
This is simple Bridge that reads a Nagios Status file and transform it into JSON documents
so it can be exposed to the Grafana JSON Datasource Plugin.
It allows you to create a Dashboard that would include a Panel of type Table containing
the last Hosts and Service statuses reported by Nagios.
This Bridge also supports filtering : the filters are given as JSON document in the Grafana Query Panel.
"""
import argparse
import threading
import atexit
import logging
import traceback
import sys
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

    logging.basicConfig(level=logging.DEBUG if args.verbosity else logging.ERROR)

    reader = nfr.NagiosFileReader(args.nagios_status_file)

    # Init
    host_status, svc_status = reader.read_status()

    # Create and start the background Thread that will read the Nagios status file
    def interrupt():
        logging.debug('interrupt')
        reader_thread.cancel()

    def refresh_data():
        global reader_thread, host_status, svc_status
        logging.debug('refresh_data active threads={threading.active_count()}, current={threading.current_thread()}')

        with data_lock:
            host_status, svc_status = reader.read_status()

        reader_thread = threading.Timer(args.interval, refresh_data, ())
        reader_thread.start()

    data_lock = threading.Lock()
    reader_thread = threading.Timer(args.interval, refresh_data, ())
    reader_thread.start()
    atexit.register(interrupt)

    # Create the Web Server and handle the requests
    api = Flask(__name__)

    @api.route('/', methods=['GET'])
    def home():
        return json.dumps({"status": "OK"})

    @api.route('/search', methods=['POST'])
    def search():
        req = request.get_json()
        logging.debug("/search", req)
        metrics = ["nagios_host_status", "nagios_service_status"]
        return json.dumps(metrics)

    @api.route('/query', methods=['POST'])
    def query():
        req = request.get_json()
        logging.debug('/query', req)
        results = {}
        with data_lock:
            try:
                type = req['targets'][0]['type']
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

        return json.dumps(results)

    return api


# Gunicorn entry point generator
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


