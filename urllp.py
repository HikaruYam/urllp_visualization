import subprocess as sp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

def show_urllp():
    i = 0
    t0, t1, t2, t4 = 0, 0, 0, 0
    plt.figure(figsize=(10, 6))
    while(True):
        t0 = time.time()
        #tcpdump generate test.pcap
        #sp.run("echo tcpdump", shell=True)
        sp.run("sudo tcpdump src host 10.10.81.50 -i eno2 -w capture.pcap -W 1 -c 2000", shell=True)
        t1 = time.time() 
        print("tcpdump finish ", t1-t0, "sec")
        #tcpdump -i eno2 -w yam0518ats2.pcap -W 1 -G 10
        #-W 回数 -G インターバル間隔(sec)

        #nasu program execute
        #generate analysi.csv
        sp.run("python3 pcap_to_csv.py capture.pcap", shell=True)
        t2 = time.time()
        print("file translate finish ", t2-t1, "sec")
        
        #import .csv and plot a graph
        try:
            df = pd.read_csv("./analysi.csv", header=None)

            delay_data = df.values[:, 1]

            delay_data *= 1000000

            t3 = time.time()
            print("import time ", t3-t2, "sec")

            #10~130 every 2 usec
            plt.ylim([0, 600])
            plt.hist(delay_data, bins=60, range=(10, 130), rwidth=0.8, color="r")
            t4 = time.time()
            print("plot time ", t4-t3, "sec")
            plt.pause(0.01)
            print()
        except:
            pass
            
if __name__ == '__main__':
    show_urllp();
