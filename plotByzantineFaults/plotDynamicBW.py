## Plot how the bandwidth capacity is throttled.
# Show the byzantine fault injected on the server.
# plotDynamicBW.py
import csv
import numpy as np
import pylab
import sys
import matplotlib.pyplot as plt
import glob
import os
import re
import datetime
from matplotlib.backends.backend_pdf import PdfPages

dataFolder = '/Users/Chen/Box Sync/Proposal/Chen\'s Proposal/exps/byzantineFaults/exp0823/'
fileName = "bw-1440353083.csv"

bwLevels = ['1 Mbps', '1 Gbps']
tsInterval = [1440353139, 1440354327]

with open(dataFolder+fileName, 'r') as bwFile:
	bw_list = list(csv.reader(bwFile, delimiter=','))

ts = [int(x[0]) for x in bw_list if int(x[0]) > tsInterval[0] and int(x[0]) < tsInterval[1]]
bw = [2 - int(x[1]) for x in bw_list if int(x[0]) > tsInterval[0] and int(x[0]) < tsInterval[1]]

fig, ax = plt.subplots()
plt.step(ts, bw, 'k-', linewidth=2.0, markersize=8)


## Change the time stamp ticks
maxTS = tsInterval[1]
minTS = tsInterval[0]
num_intvs = int((maxTS - minTS)/20) + 1
ts_labels = [minTS + x*20 for x in range(num_intvs)]
str_ts = [datetime.datetime.fromtimestamp(x*20 + minTS).strftime('%H:%M:%S') for x in range(num_intvs)]
plt.xticks(ts_labels, str_ts, fontsize=15)

## Change the bandwidth ticks
bwInds = [1, 2]
plt.yticks(bwInds, bwLevels, fontsize=15)

ax.set_xlabel("Time", fontsize=20)
ax.set_ylabel("Server's outbound capacity", fontsize=20)

plt.ylim((0,3))
plt.xlim((minTS, minTS + 100))

box = ax.get_position()
ax.set_position([box.x0 + 0.05, box.y0 + 0.1, box.width*0.9, box.height * 0.9])

plt.show()

pdf = PdfPages(dataFolder + 'imgs/srv_bw.pdf')
pdf.savefig(fig)

pdf.close()


