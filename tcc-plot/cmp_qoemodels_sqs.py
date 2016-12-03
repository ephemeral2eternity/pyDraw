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
plt_styles = ['k-', 'b--', 'r-.', 'm-', 'y-', 'g-']
intvl = 60

## Folders and Filenames
dataFolder = 'D://GitHub/pyDraw/tcc-data/qoe-models/'
imgFolder = 'D://GitHub/pyDraw/tcc-imgs/'
client_files = {
    '6 Mbps' :
    {
        'Linear QoE': "client-03_02182129_client_linear_exp_greedy_sqs.json",
        'Cascading QoE' :"client-04_02182129_client_cascading_exp_greedy_sqs.json"
    },
    '4 Mbps':
    {
        'Linear QoE': "client-03_02182218_client_linear_exp_greedy_sqs.json",
        'Cascading QoE' :"client-04_02182218_client_cascading_exp_greedy_sqs.json"
    },
    '2 Mbps':
    {
        'Linear QoE': "client-03_02182241_client_linear_exp_greedy_sqs.json",
        'Cascading QoE' :"client-04_02182241_client_cascading_exp_greedy_sqs.json"
    }
}

anomaly_file = "cache-02-anomalies.csv"
anomaly_info = read_anomaly_info(dataFolder+anomaly_file)

srv_name_mapping = {"cache-02" : "A", "cache-04": "B", "cache-06" : "C"}

## Compare Server QoE Scores
# Load SQS Data
for bw in client_files.keys():
    linear_sqs_file = client_files[bw]['Linear QoE']
    cascading_sqs_file = client_files[bw]['Cascading QoE']
    linear_sqs_data = json.load(open(dataFolder + linear_sqs_file))
    cascading_sqs_data = json.load(open(dataFolder + cascading_sqs_file))

    linear_ts, linear_candidates, linear_sqs = loadSQS(linear_sqs_data)
    cascading_ts, cascading_candidates, cascading_sqs = loadSQS(cascading_sqs_data)

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

    srv_ind = 0
    axarr[0].set_title("Linear QoE based SQS")
    for srv in linear_candidates:
        axarr[0].plot(linear_ts, linear_sqs[srv], plt_styles[srv_ind], label=srv_name_mapping[srv])
        srv_ind += 1

    srv_ind = 0
    axarr[1].set_title("Cascading QoE based SQS")
    for srv in cascading_candidates:
        axarr[1].plot(cascading_ts, cascading_sqs[srv], plt_styles[srv_ind], label=srv_name_mapping[srv])
        srv_ind += 1

    minTS = min(min(linear_ts), min(cascading_ts))
    maxTS = max(max(linear_ts), max(cascading_ts))
    num_intvls = int((maxTS - minTS)/intvl) + 1
    ts_labels = [minTS + x*intvl for x in range(num_intvls)]
    # str_ts = [datetime.datetime.fromtimestamp(x*intvl + minTS).strftime('%H:%M') for x in range(num_intvls)]
    str_ts = [time.strftime("%H:%M", time.gmtime(x*intvl)) for x in range(num_intvls)]

    qoe_labels = range(1,6)
    str_qoe = ["Bad", "Poor", "Fair", "Good", "Excellent"]

    for cur_ax in axarr:
        plt.setp(cur_ax, xticks=ts_labels, xticklabels=str_ts,
            yticks=qoe_labels, yticklabels=str_qoe)
        cur_ax.set_ylim((0,6))
        cur_ax.set_xlim((minTS, maxTS))
        cur_ax.legend(loc=4)

        ## Label anomalies
        anomaly_ind = 0
        for anomaly_ts in anomaly_info.keys():
            if (float(anomaly_ts) > minTS) and (float(anomaly_ts) < maxTS):
                anomaly_server = anomaly_info[anomaly_ts]['Server']
                anomaly_bw = int(anomaly_info[anomaly_ts]['Parameter'])/1000
                anomaly_str = "Server " + anomaly_server + "\nBandwidth:" + str(anomaly_bw) + " Mbps"
                cur_ax.annotate(anomaly_str, xy=(anomaly_ts, 0), xytext=(anomaly_ts, 2), color="red",
                        arrowprops=dict(facecolor="red", shrink=0.05, width=2))
            anomaly_ind += 1

    ax.set_xlabel("Time", fontsize=15)
    ax.set_ylabel("Server QoE Score(0-5)", fontsize=15, position=(-0.4, 0.5))

    pdf = PdfPages(imgFolder + 'cmp_qoemodels_sqs_' + bw + '.pdf')
    pdf.savefig(fig)
    pdf.close()
    plt.savefig(imgFolder + 'cmp_qoemodels_sqs_' + bw + '.png')
    plt.savefig(imgFolder + 'cmp_qoemodels_sqs_' + bw + '.jpg')

    # fig.subplots_adjust(left=0.5)
    plt.show()
