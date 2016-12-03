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
dataFolder = 'D://GitHub/pyDraw/tcc-data/sqs-exps/'
imgFolder = 'D://GitHub/pyDraw/tcc-imgs/'
client_files = {
    'Stationary' :
    {
        'Averaging': "client-03_02201316_client_cascading_ave_greedy_sqs.json",
        'Weighted averaging' :"client-03_02201332_client_cascading_exp_greedy_sqs.json"
    },
    'Non-stationary':
    {
        'Averaging': "client-03_02201421_client_cascading_ave_greedy_sqs.json",
        'Weighted averaging' :"client-03_02201433_client_cascading_exp_greedy_sqs.json"
    }
}

bw_change_file = "bw-change.csv"
bw_change_info = read_bw_change_info(dataFolder+bw_change_file)

srv_name_mapping = {"cache-02" : "A", "cache-04": "B", "cache-06" : "C"}
srv_color = {"A":"r", "B":"b","C":"k"}
qoe_labels = range(1,6)
str_qoe = ["Bad", "Poor", "Fair", "Good", "Excellent"]

## Compare Server QoE Scores
# Load SQS Data
for case in client_files.keys():
    ave_sqs_file = client_files[case]['Averaging']
    exp_sqs_file = client_files[case]['Weighted averaging']
    ave_sqs_data = json.load(open(dataFolder + ave_sqs_file))
    exp_sqs_data = json.load(open(dataFolder + exp_sqs_file))

    ave_ts, ave_candidates, ave_sqs = loadSQS(ave_sqs_data)
    exp_ts, exp_candidates, exp_sqs = loadSQS(exp_sqs_data)

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

    axarr[0].set_title("The averaging SQS learning")
    for srv in ave_candidates:
        axarr[0].plot(ave_ts, ave_sqs[srv], plt_styles[srv_name_mapping[srv]], label=srv_name_mapping[srv])

    ave_minTS = min(ave_ts)
    ave_maxTS = max(ave_ts)
    num_intvls = int((ave_maxTS - ave_minTS)/intvl) + 1
    ts_labels = [ave_minTS + x*intvl for x in range(num_intvls)]
    # str_ts = [datetime.datetime.fromtimestamp(x*intvl + minTS).strftime('%H:%M') for x in range(num_intvls)]
    str_ts = [time.strftime("%H:%M", time.gmtime(x*intvl)) for x in range(num_intvls)]
    plt.setp(axarr[0], xticks=ts_labels, xticklabels=str_ts, yticks=qoe_labels, yticklabels=str_qoe)
    axarr[0].set_ylim((0,6))
    axarr[0].set_xlim((ave_minTS, ave_maxTS))
    axarr[0].legend(loc=4)

    height = 0
    delta = 1
    for bw_change_ts in bw_change_info.keys():
        if (float(bw_change_ts) > ave_minTS) and (float(bw_change_ts) < ave_maxTS):
            bw_change_server = bw_change_info[bw_change_ts]['Server']
            org_bw = int(bw_change_info[bw_change_ts]['orgBW'])/1000
            cur_bw = int(bw_change_info[bw_change_ts]['curBW'])/1000
            anomaly_str = "Server " + bw_change_server + "\n" + str(org_bw) \
                          + " Mbps -> " + str(cur_bw) + "Mbps"
            axarr[0].annotate(anomaly_str, xy=(bw_change_ts, height), xytext=(bw_change_ts, height+delta), color=srv_color[bw_change_server],
                    arrowprops=dict(facecolor=srv_color[bw_change_server], shrink=0.05, width=2))
            height += 3.5*delta

    axarr[1].set_title("The weighted averaging SQS learning")
    for srv in exp_candidates:
        axarr[1].plot(exp_ts, exp_sqs[srv], plt_styles[srv_name_mapping[srv]], label=srv_name_mapping[srv])

    exp_minTS = min(exp_ts)
    exp_maxTS = max(exp_ts)
    num_intvls = int((exp_maxTS - exp_minTS)/intvl) + 1
    ts_labels = [exp_minTS + x*intvl for x in range(num_intvls)]
    # str_ts = [datetime.datetime.fromtimestamp(x*intvl + minTS).strftime('%H:%M') for x in range(num_intvls)]
    str_ts = [time.strftime("%H:%M", time.gmtime(x*intvl)) for x in range(num_intvls)]
    plt.setp(axarr[1], xticks=ts_labels, xticklabels=str_ts, yticks=qoe_labels, yticklabels=str_qoe)
    axarr[1].set_ylim((0,6))
    axarr[1].set_xlim((exp_minTS, exp_maxTS))
    axarr[1].legend(loc=4)

    ## Label anomalies
    height = 0
    delta = 1
    for bw_change_ts in bw_change_info.keys():
        if (float(bw_change_ts) > exp_minTS) and (float(bw_change_ts) < exp_maxTS):
            bw_change_server = bw_change_info[bw_change_ts]['Server']
            org_bw = int(bw_change_info[bw_change_ts]['orgBW'])/1000
            cur_bw = int(bw_change_info[bw_change_ts]['curBW'])/1000
            anomaly_str = "Server " + bw_change_server + "\n" + str(org_bw) \
                          + " Mbps -> " + str(cur_bw) + "Mbps"
            axarr[1].annotate(anomaly_str, xy=(bw_change_ts, height), xytext=(bw_change_ts, height+delta), color=srv_color[bw_change_server],
                    arrowprops=dict(facecolor=srv_color[bw_change_server], shrink=0.05, width=2))
            height += 3.5*delta

    ax.set_xlabel("Time", fontsize=15)
    ax.set_ylabel("Server QoE Score(0-5)", fontsize=15, position=(-0.4, 0.5))
    # ax.set_title(case, fontsize=15)

    pdf = PdfPages(imgFolder + 'cmp_qoemodels_sqs_' + case + '.pdf')
    pdf.savefig(fig)
    pdf.close()
    plt.savefig(imgFolder + 'cmp_qoemodels_sqs_' + case + '.png')
    plt.savefig(imgFolder + 'cmp_qoemodels_sqs_' + case + '.jpg')

    # fig.subplots_adjust(left=0.5)
    plt.show()
