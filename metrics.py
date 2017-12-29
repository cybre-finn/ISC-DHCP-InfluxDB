from isc_dhcp_leases import Lease, IscDhcpLeases
from influxdb import InfluxDBClient
import requests
import socket
import datetime

def setup_request():
    time = datetime.datetime.now().isoformat()
    leases = IscDhcpLeases('dump_dhcpd.leases')
    leases_count = print(len(leases.get()))
    hostname = (socket.gethostname())
    json_body = [
    {
    "measurement": "dhcp_leases_count",
    "tags": {
    "host": hostname,
    },
    "time": time,
    "fields": {
    "value": leases_count
    }
    }
    ]
    return json_body

def setup_influx():
    client = InfluxDBClient('192.168.10.4', 8086, '', '', '')
    client.create_database('dhcpcd')
    return client

json_body=setup_request()
client=setup_influx()
client.write_points(json_body)
exit(1)
