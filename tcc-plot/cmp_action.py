import json
import datetime
from loadData.loadQoE import *
from loadData.readAnomaly import *
import numpy as np
import pylab
import sys
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

## Utilities
plt_styles = {"A":"r-.", "B":"b--","C":"k-"}
intvl = 60

## Folders and Filenames
dataFolder = 'D://GitHub/pyDraw/tcc-data/action-exps/'
imgFolder = 'D://GitHub/pyDraw/tcc-imgs/'
client_files = {
    'Epsilon-Greedy' :"client-03_02201502_client_cascading_exp_epsilon_sqs.json",
    'Greedy': "client-03_02201512_client_cascading_exp_greedy_sqs.json"
}

bw_change_file = "bw-change.csv"
bw_change_info = read_bw_change_info(dataFolder+bw_change_file)

srv_name_mapping = {"cache-02" : "A", "cache-04": "B", "cache-06" : "C"}
srv_color = {"A":"r", "B":"b","C":"k"}
qoe_labels = range(1,6)
str_qoe = ["Bad", "Poor", "Fair", "Good", "Excellent"]

# Plot linear SQS
fig = plt.figure()
ax = fig.add_subplot(111)    # The big subplot
#pos = ax.get_position()
#new_pos = [pos.x0, pos.y0, pos.width, pos.height]
#ax.set_position(new_pos)
axarr = []
ax1 = fig.add_subplot(211)
pos1 = ax1.get_position()
new_pos1 = [pos1.x0 + 0.1, pos1.y0, pos1.width - 0.1, pos1.height]
ax1.set_position(new_pos1)
ax2 = fig.add_subplot(212)
pos2 = ax2.get_position()
new_pos2 = [pos2.x0 + 0.1, pos2.y0, pos2.width - 0.1, pos2.height]
ax2.set_position(new_pos2)
axarr.append(ax1)
axarr.append(ax2)

# Turn off axis lines and ticks of the big subplot
ax.spines['top'].set_color('none')
ax.spines['bottom'].set_color('none')
ax.spines['left'].set_color('none')
ax.spines['right'].set_color('none')
ax.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off')

method_id = 0
## Compare Server QoE Scores
# Load SQS Data
for method in client_files.keys():
    sqs_file = client_files[method]
    sqs_data = json.load(open(dataFolder + sqs_file))

    ts, candidates, sqs = loadSQS(sqs_data)

    axarr[method_id].set_title(method)
    for srv in candidates:
        axarr[method_id].plot(ts, sqs[srv], plt_styles[srv_name_mapping[srv]], label=srv_name_mapping[srv])

    minTS = min(ts)
    maxTS = max(ts)
    num_intvls = int((maxTS - minTS)/intvl) + 1
    ts_labels = [minTS + x*intvl for x in range(num_intvls)]
    # str_ts = [datetime.datetime.fromtimestamp(x*intvl + minTS).strftime('%H:%M') for x in range(num_intvls)]
    str_ts = [time.strftime("%H:%M", time.gmtime(x*intvl)) for x in range(num_intvls)]
    plt.setp(axarr[method_id], xticks=ts_labels, xticklabels=str_ts, yticks=qoe_labels, yticklabels=str_qoe)
    axarr[method_id].set_ylim((0,6))
    axarr[method_id].set_xlim((minTS, maxTS))
    axarr[method_id].legend(loc=4)

    height = 0
    delta = 1
    for bw_change_ts in bw_change_info.keys():
        if (float(bw_change_ts) > minTS) and (float(bw_change_ts) < maxTS):
            bw_change_server = bw_change_info[bw_change_ts]['Server']
            org_bw = int(bw_change_info[bw_change_ts]['orgBW'])/1000
            cur_bw = int(bw_change_info[bw_change_ts]['curBW'])/1000
            anomaly_str = "Server " + bw_change_server + "\n" + str(org_bw) \
                          + " Mbps -> " + str(cur_bw) + "Mbps"
            axarr[method_id].annotate(anomaly_str, xy=(bw_change_ts, height), xytext=(bw_change_ts, height+delta), color=srv_color[bw_change_server],
                    arrowprops=dict(facecolor=srv_color[bw_change_server], shrink=0.05, width=2))
            height += 3.5*delta

    method_id += 1

ax.set_xlabel("Time", fontsize=15)
ax.set_ylabel("Server QoE Score(0-5)", fontsize=15, position=(-0.4, 0.5))
# ax.set_title(case, fontsize=15)

pdf = PdfPages(imgFolder + 'cmp_action_sqs.pdf')
pdf.savefig(fig)
pdf.close()
plt.savefig(imgFolder + 'cmp_action_sqs.png')
plt.savefig(imgFolder + 'cmp_action_sqs.jpg')

# fig.subplots_adjust(left=0.5)
plt.show()
