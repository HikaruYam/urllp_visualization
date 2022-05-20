import subprocess as sp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#tcpdump generate test.pcap
sp.run("echo tcpdump", shell=True)
print("finish")
#tcpdump -i eno2 -w yam0518ats2.pcap -W1 -G10

#nasu program execute
#generate analysi.csv
sp.run("python3 pcap_to_csv.py test.pcap", shell=True)

#import .csv and plot a graph
df = pd.read_csv("./analysi.csv", header=None)

print(df.values[:, 1])

delay_data = df.values[:, 1]

#10~130 every 2 usec
plt.hist(delay_data, bins=60, range(10, 130), rwidth=0.8)