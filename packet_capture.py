import zerorpc
import sys
from scapy.all import *
import json

packets_pool = []
exit_code = False


class PacketApi(object):

    def __init__(self):
        self.packet_thread = ServerThread("")

    def start_capture(self, sniff_filter):
        self.packet_thread = ServerThread(sniff_filter)
        self.packet_thread.start()
        print('get request {}'.format(sniff_filter))
        return json.dumps({
            'code': 0,
            'msg': 'START capture packets...'
        })

    def stop_capture(self):
        self.packet_thread.set_exit_code(True)
        self.packet_thread.join()
        return json.dumps({
            'code': 0,
            'msg': 'STOP capture packets...'
        })

    @staticmethod
    def get_packets():
        while len(packets_pool) == 0:
            pass
        pkt = packets_pool.pop(0)

        try:
            raw_load = str(pkt['Raw'].load)
        except IndexError:
            raw_load = 'None'

        try:
            padding_load = str(pkt['Padding'].load)
        except IndexError:
            padding_load = 'None'

        try:
            if pkt[IP]:
                ip_version = 'IP'
        except IndexError:
            ip_version = 'IPv6'

        try:
            if pkt[TCP]:
                protoc = 'TCP'
        except IndexError:
            protoc = 'UDP'

        if protoc is 'TCP':
            try:
                pkt_json = json.dumps({
                    'dst': pkt['Ether'].dst,
                    'src': pkt['Ether'].src,
                    'type': pkt['Ether'].type,
                    'version': pkt[ip_version].version,
                    'len': pkt[ip_version].len,
                    'id': pkt[ip_version].id,
                    'proto': 'tcp',
                    'chksum': pkt[ip_version].chksum,
                    'ipSrc': pkt[ip_version].src,
                    'ipDst': pkt[ip_version].dst,
                    'sport': pkt[protoc].sport,
                    'rawLoad': raw_load,
                    'paddingLoad': padding_load

                })
            except IndexError:
                pkt.show()
                pkt_json = "None"
            except AttributeError:
                pkt.show()
                pkt_json = "None"
            return pkt_json
        else:
            try:
                pkt_json = json.dumps({
                    'dst': pkt['Ether'].dst,
                    'src': pkt['Ether'].src,
                    'type': pkt['Ether'].type,
                    'version': pkt[ip_version].version,
                    'len': pkt[ip_version].len,
                    'id': pkt[ip_version].id,
                    'proto': 'udp',
                    'chksum': pkt[ip_version].chksum,
                    'ipSrc': pkt[ip_version].src,
                    'ipDst': pkt[ip_version].dst,
                    'sport': pkt[protoc].sport,
                    'rawLoad': raw_load,
                    'paddingLoad': padding_load

                })
            except IndexError:
                pkt.show()
                pkt_json = "None"
            except AttributeError:
                pkt.show()
                pkt_json = "None"
            return pkt_json


class ServerThread(threading.Thread):
    def __init__(self, sniff_filter):
        super().__init__()
        self.sniff_filter = sniff_filter
        self.exit_code = False

    def run(self):
        while not self.exit_code:
            packets = sniff(filter=self.sniff_filter, iface="en0", count=1)
            for pkt in packets:
                packets_pool.append(pkt)
        print('stopping...')

    def set_exit_code(self, exit_code):
        self.exit_code = exit_code

    def set_filter(self, sniff_filter):
        self.sniff_filter = sniff_filter


def main():
    addr = 'tcp://127.0.0.1:8888'
    s = zerorpc.Server(PacketApi())
    s.bind(addr)
    print('start running on {}'.format(addr))
    s.run()


if __name__ == '__main__':
    main()
