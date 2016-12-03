import json
import datetime
from loadData.loadQoE import *
from loadData.readAnomaly import *
import numpy as np
import pylab
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

## Utilities
plt_styles = ['k-', 'b--', 'r-.', 'm-', 'y-', 'g-']
intvl = 60

## Folders and Filenames
dataFolder = 'D://GitHub/pyDraw/tcc-data/qoe-models/'

'''
## Throttle bandwidth to 6Mbps
linear_client_file = "client-03_02182241_client_linear_exp_greedy.json"
linear_sqs_file = "client-03_02182241_client_linear_exp_greedy_sqs.json"
cascading_client_file = "client-04_02182241_client_cascading_exp_greedy.json"
cascading_sqs_file = "client-04_02182241_client_cascading_exp_greedy_sqs.json"


## Throttle bandwidth to 4Mbps
linear_client_file = "client-03_02182218_client_linear_exp_greedy.json"
linear_sqs_file = "client-03_02182218_client_linear_exp_greedy_sqs.json"
cascading_client_file = "client-04_02182218_client_cascading_exp_greedy.json"
cascading_sqs_file = "client-04_02182218_client_cascading_exp_greedy_sqs.json"
'''
'''
'''
## Throttle bandwidth to 2Mbps
linear_client_file = "client-03_02182129_client_linear_exp_greedy.json"
linear_sqs_file = "client-03_02182129_client_linear_exp_greedy_sqs.json"
cascading_client_file = "client-04_02182129_client_cascading_exp_greedy.json"
cascading_sqs_file = "client-04_02182129_client_cascading_exp_greedy_sqs.json"


anomaly_file = "anomaly.csv"
cache_agents_file = "cache_agents.json"

## Load Data
linear_client_data = json.load(open(dataFolder + linear_client_file))
linear_sqs_data = json.load(open(dataFolder + linear_sqs_file))
cascading_client_data = json.load(open(dataFolder + cascading_client_file))
cascading_sqs_data = json.load(open(dataFolder + cascading_sqs_file))
cache_agents = json.load(open(dataFolder+cache_agents_file))
anomaly_info = read_anomaly_info(dataFolder+anomaly_file)

'''
## Compare QoE over time and draw the start of bandwidth throttling
linear_ts, linear_qoes = getTimeQoE(linear_client_data, QoE="linear")
cascading_ts, cascading_qoes = getTimeQoE(cascading_client_data, QoE="cascading")

fig, ax = plt.subplots()
plt.plot(linear_ts, linear_qoes, plt_styles[0], label="Linear QoE model")
plt.plot(cascading_ts, cascading_qoes, plt_styles[1], label="Cascading QoE model")
minTS = min(min(linear_ts), min(cascading_ts))
maxTS = max(max(linear_ts), max(cascading_ts))
num_intvls = int((maxTS - minTS)/intvl) + 1
ts_labels = [minTS + x*intvl for x in range(num_intvls)]
str_ts = [datetime.datetime.fromtimestamp(x*intvl + minTS).strftime('%H:%M') for x in range(num_intvls)]

qoe_labels = range(1,6)
str_qoe = ["Bad", "Poor", "Fair", "Good", "Excellent"]
plt.xticks(ts_labels, str_ts, fontsize=15)
plt.yticks(qoe_labels, str_qoe, fontsize=15)

ax.set_xlabel("Time", fontsize=20)
ax.set_ylabel("Chunk Response Time(secondes)", fontsize=20)

## Label anomalies
anomaly_ind = 0
for anomaly_ts in anomaly_info.keys():
    anomaly_server = anomaly_info[anomaly_ts]['Server']
    anomaly_bw = int(anomaly_info[anomaly_ts]['Parameter'])/1000
    anomaly_str = "Server " + anomaly_server + "\nBandwidth:" + str(anomaly_bw) + " Mbps"
    ax.annotate(anomaly_str, xy=(anomaly_ts, 0), xytext=(anomaly_ts, 1), color="red",
            arrowprops=dict(facecolor="red", shrink=0.05, width=2))
    anomaly_ind += 1

plt.ylim((0,6))
plt.xlim((minTS, maxTS))
plt.legend()
plt.show()
'''

## Compare Server QoE Scores
# Load SQS Data
linear_ts, linear_candidates, linear_sqs = loadSQS(linear_sqs_data)
cascading_ts, cascading_candidates, cascading_sqs = loadSQS(cascading_sqs_data)

# Plot linear SQS
fig = plt.figure()
ax = fig.add_subplot(111)    # The big subplot
axarr = []
axarr.append(fig.add_subplot(211))
axarr.append(fig.add_subplot(212))

# Turn off axis lines and ticks of the big subplot
ax.spines['top'].set_color('none')
ax.spines['bottom'].set_color('none')
ax.spines['left'].set_color('none')
ax.spines['right'].set_color('none')
ax.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off')

srv_ind = 0
axarr[0].set_title("Linear QoE based SQS")
for srv in linear_candidates:
    axarr[0].plot(linear_ts, linear_sqs[srv], plt_styles[srv_ind], label=srv)
    srv_ind += 1

srv_ind = 0
axarr[1].set_title("Cascading QoE based SQS")
for srv in cascading_candidates:
    axarr[1].plot(cascading_ts, cascading_sqs[srv], plt_styles[srv_ind], label=srv)
    srv_ind += 1

minTS = min(min(linear_ts), min(cascading_ts))
maxTS = max(max(linear_ts), max(cascading_ts))
num_intvls = int((maxTS - minTS)/intvl) + 1
ts_labels = [minTS + x*intvl for x in range(num_intvls)]
str_ts = [datetime.datetime.fromtimestamp(x*intvl + minTS).strftime('%H:%M') for x in range(num_intvls)]

qoe_labels = range(1,6)
str_qoe = ["Bad", "Poor", "Fair", "Good", "Excellent"]

for cur_ax in axarr:
    plt.setp(cur_ax, xticks=ts_labels, xticklabels=str_ts,
        yticks=qoe_labels, yticklabels=str_qoe)
    cur_ax.set_ylim((0,6))
    cur_ax.set_xlim((minTS, maxTS))
    cur_ax.legend(loc=0)

ax.set_xlabel("Time", fontsize=15)
ax.set_ylabel("Server QoE Score(0-5)", fontsize=15, position=(-0.4, 0.5))

plt.show()



