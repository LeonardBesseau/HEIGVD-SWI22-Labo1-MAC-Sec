import argparse

from scapy.all import *
# Args parsing
from scapy.layers.dot11 import Dot11Elt

parser = argparse.ArgumentParser(prog="Station Access point detection",
                                 usage="client_network_detect.py -i wlp2s0mon",
                                 allow_abbrev=False)

parser.add_argument("-i", "--Interface", required=True,
                    help="The interface that you want to use, needs to be set to monitor mode")
parser.add_argument("-s", "--SSID", required=False,
                    help="The SSID to filter for",
                    default=None)

args = parser.parse_args()

BSSID_to_SSID = {}


def packet_handler(p):
    if p.FCfield & 0x1 != 0 or p.FCfield & 0x2 != 0:
        return

    if p.haslayer(Dot11Elt) and str(p.addr3) not in BSSID_to_SSID and len(p.info) > 0:
        BSSID_to_SSID[str(p.addr3)] = p.info

    # Ignore broadcast
    if str(p.addr3) == "ff:ff:ff:ff:ff:ff" or str(p.addr3) == "None" or (
            p.addr2 == p.addr3 and str(p.addr1) == "ff:ff:ff:ff:ff:ff"):
        return

    if args.SSID is None or args.SSID == p.info.decode('utf-8'):
        if p.addr3 == p.addr2:
            display_info(str(p.addr1), str(p.addr3))
        else:
            display_info(str(p.addr2), str(p.addr3))


def display_info(sta, bssid):
    print("{}    {}".format(sta, bssid))


sniff(iface=args.Interface, prn=packet_handler)
