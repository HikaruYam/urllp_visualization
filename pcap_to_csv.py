import dpkt
import struct
import socket
import csv
import string
import binascii
import sys

def main(filename):
    pcr = dpkt.pcap.Reader(open(filename, 'rb'))

    with open('analysi.csv', 'w') as analysis:
        for ts, buf in pcr:
            try:
                eth = dpkt.ethernet.Ethernet(buf)
            except:
                continue

            if type(eth.data) == dpkt.ip.IP:
                ip = eth.data
                src = socket.inet_ntoa(ip.src)

                if type(ip.data) == dpkt.udp.UDP:
                    udp = ip.data
                    if len(udp.data) != 0:
                        uhex = binascii.b2a_hex(udp.data)
                        total_sec = uhex[-64:-56]
                        total_usec = uhex[-56:-48]
                        in_sec = uhex[-48:-40]
                        in_usec = uhex[-40:-32]
                        out_sec = uhex[-32:-24]
                        out_usec = uhex[-24:-16]
                        total_ = cal(total_sec, total_usec)
                        in_ = cal(in_sec, in_usec)
                        out_ = cal(out_sec, out_usec)
                        total_ = round((total_ + (out_ - in_)), 6)
                        writer = csv.writer(analysis, lineterminator='\n')
                        writer.writerow([src, str(total_)])

def cal(sec, usec):
    sec = sec[-2:] + sec[-4:-2] + sec[-6:-4] + sec[-8:-6]
    usec = usec[-2:] + usec[-4:-2] + usec[-6:-4] + usec[-8:-6]
    sec = int(sec, 16)
    usec = int(usec, 16)
    sec = str(sec)
    usec = str(usec)
    usec = usec.zfill(6)
    total = sec + '.' + usec
    total = float(total)
    return total

if __name__ == '__main__':
    if (len((sys.argv)) != 2):
        print("Error")
        exit()
    filename = sys.argv[1]
    main(filename)

