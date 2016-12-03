import json
import datetime
from loadData.loadQoE import *
from loadData.readAnomaly import *
import numpy as np
import pylab
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

plt_styles = ['k-', 'b--', 'r-.', 'm-', 'y-', 'g-']
intvl = 60
dataFolder = 'D://GitHub/pyDraw/tcc-data/qoe-models/'
imgFolder = 'D://GitHub/pyDraw/tcc-imgs/'
client_files = {
    '6 Mbps' :
    {
        'Linear QoE': "client-03_02182129_client_linear_exp_greedy.json",
        'Cascading QoE' :"client-04_02182129_client_cascading_exp_greedy.json"
    },
    '4 Mbps':
    {
        'Linear QoE': "client-03_02182218_client_linear_exp_greedy.json",
        'Cascading QoE' :"client-04_02182218_client_cascading_exp_greedy.json"
    },
    '2 Mbps':
    {
        'Linear QoE': "client-03_02182241_client_linear_exp_greedy.json",
        'Cascading QoE' :"client-04_02182241_client_cascading_exp_greedy.json"
    }
}

anomaly_file = "cache-02-anomalies.csv"
anomaly_info = read_anomaly_info(dataFolder+anomaly_file)

'''
# Create subplots
fig = plt.figure()
ax = fig.add_subplot(111)    # The big subplot
axarr = []
axarr.append(fig.add_subplot(311))
axarr.append(fig.add_subplot(312))
axarr.append(fig.add_subplot(313))

# Turn off axis lines and ticks of the big subplot
ax.spines['top'].set_color('none')
ax.spines['bottom'].set_color('none')
ax.spines['left'].set_color('none')
ax.spines['right'].set_color('none')
ax.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off')


plt_ind = 0
## Compare Chunk Bitrates
for bw in client_files.keys():
    linear_file = client_files[bw]['Linear QoE']
    cascading_file = client_files[bw]['Cascading QoE']
    linear_client_data = json.load(open(dataFolder + linear_file))
    cascading_client_data = json.load(open(dataFolder + cascading_file))
    linear_ts, linear_bitrates = getTimeBitrate(linear_client_data)
    cascading_ts, cascading_bitrates = getTimeBitrate(cascading_client_data)

    axarr[plt_ind].scatter(linear_ts, linear_bitrates,  marker = 'x', color = 'k', label="Linear QoE model")
    axarr[plt_ind].scatter(cascading_ts, cascading_bitrates, marker = 'o', color = 'b', label="Cascading QoE model")

    minTS = min(min(linear_ts), min(cascading_ts))
    maxTS = max(max(linear_ts), max(cascading_ts))
    num_intvls = int((maxTS - minTS)/intvl) + 1
    ts_labels = [minTS + x*intvl for x in range(num_intvls)]
    str_ts = [datetime.datetime.fromtimestamp(x*intvl + minTS).strftime('%H:%M') for x in range(num_intvls)]

    plt.setp(axarr[plt_ind], xticks=ts_labels, xticklabels=str_ts)
    axarr[plt_ind].set_ylim((0,10))
    axarr[plt_ind].set_xlim((minTS, maxTS))
    axarr[plt_ind].legend(loc=4)


    ## Label anomalies
    anomaly_ind = 0
    for anomaly_ts in anomaly_info.keys():
        if (float(anomaly_ts) > minTS) and (float(anomaly_ts) < maxTS):
            anomaly_server = anomaly_info[anomaly_ts]['Server']
            anomaly_bw = int(anomaly_info[anomaly_ts]['Parameter'])/1000
            anomaly_str = "Server " + anomaly_server + "\nBandwidth:" + str(anomaly_bw) + " Mbps"
            axarr[plt_ind].annotate(anomaly_str, xy=(anomaly_ts, 0), xytext=(anomaly_ts, 2), color="red",
                    arrowprops=dict(facecolor="red", shrink=0.05, width=2))
        anomaly_ind += 1


    plt_ind += 1
'''

fig, ax = plt.subplots()
bw = '2 Mbps'

linear_file = client_files[bw]['Linear QoE']
cascading_file = client_files[bw]['Cascading QoE']
linear_client_data = json.load(open(dataFolder + linear_file))
cascading_client_data = json.load(open(dataFolder + cascading_file))
linear_ts, linear_bitrates = getTimeBitrate(linear_client_data)
cascading_ts, cascading_bitrates = getTimeBitrate(cascading_client_data)

ax.scatter(linear_ts, linear_bitrates,  marker = 'x', color = 'k', label="Linear QoE model")
ax.scatter(cascading_ts, cascading_bitrates, marker = 'o', color = 'b', label="Cascading QoE model")

minTS = min(min(linear_ts), min(cascading_ts))
maxTS = max(max(linear_ts), max(cascading_ts))
num_intvls = int((maxTS - minTS)/intvl) + 1
ts_labels = [minTS + x*intvl for x in range(num_intvls)]
str_ts = [datetime.datetime.fromtimestamp(x*intvl + minTS).strftime('%H:%M') for x in range(num_intvls)]

plt.setp(ax, xticks=ts_labels, xticklabels=str_ts)
ax.set_ylim((0,10))
ax.set_xlim((minTS, maxTS))
ax.legend(loc=4)


## Label anomalies
anomaly_ind = 0
for anomaly_ts in anomaly_info.keys():
    if (float(anomaly_ts) > minTS) and (float(anomaly_ts) < maxTS):
        anomaly_server = anomaly_info[anomaly_ts]['Server']
        anomaly_bw = int(anomaly_info[anomaly_ts]['Parameter'])/1000
        anomaly_str = "Server " + anomaly_server + "\nBandwidth:" + str(anomaly_bw) + " Mbps"
        ax.annotate(anomaly_str, xy=(anomaly_ts, 0), xytext=(anomaly_ts, 1), color="red",
                arrowprops=dict(facecolor="red", shrink=0.05, width=2))
    anomaly_ind += 1


ax.set_xlabel("Time", fontsize=15)
ax.set_ylabel("Chunk Bitrate Levels (1-9)", fontsize=15)

plt.show()

pdf = PdfPages(imgFolder + 'cmp_qoemodels_bitrates_2mbps.pdf')
pdf.savefig(fig)
pdf.close()

plt.savefig(imgFolder + 'cmp_qoemodels_bitrates_2mbps.png')

'''

plt.ylim((0,10))
plt.xlim((minTS, maxTS))
plt.legend()
plt.show()
'''