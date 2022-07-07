import subprocess as sp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

def show_urllp():
    i = 0
    t0, t1, t2, t4 = 0, 0, 0, 0
    plt.figure(figsize=(20, 6))
    while(True):
        t0 = time.time()
        #tcpdump generate test.pcap
        #sp.run("echo tcpdump", shell=True)
        sp.run("sudo tcpdump src host 10.10.81.50 -i eno2 -w capture.pcap -W 1 -c 1000", shell=True)
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

            #10~130 every 1000 packet
            
            plt.subplot(1, 2, 1)
            plt.title("Proposed method")
            plt.ylabel("number of packet")
            plt.xlabel("delay [μsec]")
            plt.ylim([0, 500])
            plt.hist(delay_data, bins=60, range=(10, 130), rwidth=0.8, color="darkorange")
            
            plt.subplot(1, 2, 2)
            plt.title("Proposed mathod")
            plt.ylabel("number of packet")
            plt.xlabel("delay [μsec]")
            plt.yscale("log")
            plt.ylim([1, 1000])
            plt.hist(delay_data, bins=60, range=(10, 130), rwidth=0.8, color="darkorange")
            t4 = time.time()
            print("plot time ", t4-t3, "sec")
            plt.pause(0.01)
            plt.clf()
            print()
        except:
            pass
            
if __name__ == '__main__':
    show_urllp();
