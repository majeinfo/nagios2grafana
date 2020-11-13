import argparse
from flask import Flask, json, request
import nagios_file_reader as nfr
import status_exporter as exp

parser = argparse.ArgumentParser(description='Bridge from nagios status.dat to Grafana dashboard')
parser.add_argument('-v', '--verbosity', help='increase output verbosity')
parser.add_argument('-i', '--interval', type=int, default=30, help='nagios status file analysis interval (in seconds)')
parser.add_argument('-p', '--port', type=int, dest='listen_port', default=5000, help='listening port')
parser.add_argument('--nagios-status-file', dest='nagios_status_file', required=True, help='path to nagios status file')
args = parser.parse_args()

# Infinite loop on file
reader = nfr.NagiosFileReader(args.nagios_status_file)
host_status, svc_status = reader.read_status()
host_data = exp.build_host_data(host_status)
svc_data = exp.build_svc_data(svc_status)

api = Flask(__name__)

@api.route('/', methods=['GET'])
def home():
    return json.dumps({"status": "OK"})

@api.route('/search', methods=['POST'])
def search():
    req = request.get_json()
    print(req)
    metrics = ["nagios_host_status", "nagios_service_status"]
    return json.dumps(metrics)

@api.route('/query', methods=['POST'])
def query():
    req = request.get_json()
    print(req)
    type = req['targets'][0]['type']
    print(req['targets'][0]['target'])
    # test "severity" req['targets'][0]['severity']
    if type == "table":
        if req['targets'][0]['target'] == 'nagios_host_status':
            results = host_data
        else:
            results = svc_data
    else: # metrics
        pass

    return json.dumps(results)

#api.run(port=listen_port)
api.run(port=args.listen_port, debug=True)
