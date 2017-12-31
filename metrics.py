#! /usr/bin/env python3
from isc_dhcp_leases import Lease, IscDhcpLeases
from influxdb import InfluxDBClient
import requests
import socket
import datetime
import time

def setup_request():
    time = datetime.datetime.utcnow().isoformat()
    leases = IscDhcpLeases('/var/lib/dhcp/dhcpd.leases')
    leases_count = len(leases.get_current())
    hostname = (socket.gethostname())
    print(leases_count)
    json_body = [
    {
        "measurement": "dhcp_leases",
        "tags": {
            "host": hostname,
        },
        "time": time,
        "fields": {
            "value":float(leases_count)
        }
    }
    ]
    print(json_body)
    return json_body

def setup_influx():
    try:
        client = InfluxDBClient('192.168.10.4', 8086, '', '', 'dhcpd')
        client.create_database('dhcpd')
    except Exception as e:
        logging.error(traceback.format_exc())
    return client
while True:
    json_body=setup_request()
    client=setup_influx()
    try:
        client.write_points(json_body)
    except Exception as e:
        logging.error(traceback.format_exc())
    time.sleep(5)
