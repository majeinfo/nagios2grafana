import argparse
import requests

parser = argparse.ArgumentParser(description='nagios2grafana test')
parser.add_argument('-v', '--verbosity', action='store_true',
                    help='increase output verbosity')
parser.add_argument('-u', '--url', dest='url', default='http://localhost:5000',
                    help='nagios2grafana url (ex: http://localhost:5000)')
args = parser.parse_args()

def test_status():
    resp = requests.get(args.url)
    assert resp.status_code == 200


def test_search():
    resp = requests.post(args.url + '/search')
    assert 'nagios_host_status' in resp.json()
    assert 'nagios_service_status' in resp.json()


#def test_query_bad_type():
#    data = {
#        "targets": [
#            {"target": "nagios_host_status", "type": "timeseries", "data": {}},
#        ],
#    }
#    resp = requests.post(args.url + '/query', json=data)
#    j = resp.json()
#    assert 'msg' in j and j['msg'] == 'type timeseries not supported'


def test_query_bad_target():
    data = {
        "targets": [
            {"target": "unknown_value", "type": "table", "data": {}},
        ],
    }
    resp = requests.post(args.url + '/query', json=data)
    j = resp.json()
    assert 'msg' in j and j['msg'] == 'target unknown_value not supported'


def test_query_hosts_no_filter():
    data = {
        "targets": [
            {"target": "nagios_host_status", "type": "table", "data": {}},
        ],
    }
    resp = requests.post(args.url + '/query', json=data)
    j = resp.json()
    assert j[0]['rows'][0][1] == 'bibli-mycity'


def test_query_hosts_with_simple_filter():
    data = {
        "targets": [
            {"target": "nagios_host_status", "type": "table", "data": {"host_name": "appli2-mongo1"}},
        ],
    }
    resp = requests.post(args.url + '/query', json=data)
    j = resp.json()
    assert j[0]['rows'][0][1] == 'appli2-mongo1'


def test_query_hosts_with_simple_filter2():
    data = {
        "targets": [
            {"target": "nagios_host_status", "type": "table", "data": {"current_state": "99"}},
        ],
    }
    resp = requests.post(args.url + '/query', json=data)
    j = resp.json()
    assert len(j[0]['rows']) == 0


def test_query_hosts_with_regexp_filter():
    data = {
        "targets": [
            {"target": "nagios_host_status", "type": "table", "data": {"host_name": "/appli1-.*/"}},
        ],
    }
    resp = requests.post(args.url + '/query', json=data)
    j = resp.json()
    assert len(j[0]['rows']) == 6

def test_query_hosts_with_regexp_filter_payload():
    data = {
        "targets": [
            {"target": "nagios_host_status", "type": "table", "payload": {"host_name": "/appli1-.*/"}},
        ],
    }
    resp = requests.post(args.url + '/query', json=data)
    j = resp.json()
    assert len(j[0]['rows']) == 6
