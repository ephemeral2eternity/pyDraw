import json
import datetime
from loadData.loadQoE import *
from loadData.loadSS import *
from rstPlots.save_fig import *
from loadData.readAnomaly import *
import numpy as np
import pylab
import sys
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def get_value_as_key(key_values):
    value_as_keys = {}
    for k in key_values.keys():
        v = key_values[k]
        value_as_keys[v] = k
    return value_as_keys



plt_styles = ['k-', 'b--', 'r-.', 'm-', 'y-', 'g-']
intvl = 90
dataFolder = 'D://GitHub/pyDraw/tcc-data/control-exps/'
imgFolder = 'D://GitHub/pyDraw/tcc-imgs/'
'''
client_files = {
    # 'Server side control':'planetlab2.utdallas.edu_02191030_server_qoe_cascading_exp_greedy.json',
    'Server side control':'planetlab2.utdallas.edu_02190900_server_qoe_cascading_exp_greedy.json',
    # 'Client side control':'planetlab2.utdallas.edu_02191000_client_cascading_exp_greedy.json'
    'Client side control':'planetlab2.utdallas.edu_02190830_client_cascading_exp_greedy.json'
}


client_files = {
    'Server side control':'planetlab3.arizona-gigapop.net_02191030_server_qoe_cascading_exp_greedy.json',
    'Client side control':'planetlab3.arizona-gigapop.net_02191000_client_cascading_exp_greedy.json'
}
'''
client_files = {
    'Server side control':'planetlab3.eecs.umich.edu_02190900_server_qoe_cascading_exp_greedy.json',
    'Client side control':'planetlab3.eecs.umich.edu_02190830_client_cascading_exp_greedy.json'
}

server_ip_file = 'D://GitHub/pyDraw/tcc-data/server_ips.json'

qoe_labels = range(1,6)
str_qoe = ["Bad", "Poor", "Fair", "Good", "Excellent"]

fig = plt.figure()
ax = fig.add_subplot(111)    # The big subplot
# Turn off axis lines and ticks of the big subplot
ax.spines['top'].set_color('none')
ax.spines['bottom'].set_color('none')
ax.spines['left'].set_color('none')
ax.spines['right'].set_color('none')
ax.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off')
#pos = ax.get_position()
#new_pos = [pos.x0, pos.y0, pos.width, pos.height]
#ax.set_position(new_pos)
axarr = []
axarr.append(fig.add_subplot(211))
axarr.append(fig.add_subplot(212))
'''
for ax_ind in range(len(axarr)):
    pos = axarr[ax_ind].get_position()
    new_pos = [pos.x0+0.1, pos.y0, pos.width-0.1, pos.height]
    axarr[ax_ind].set_position(new_pos)
'''

fk_srv_names = ["A", "B", "C", "D", "E"]

ctype_ind = 0
for control_type in client_files.keys():
    client_file = client_files[control_type]
    client_trace = json.load(open(dataFolder+client_file))
    server_ips = json.load(open(server_ip_file))

    ip_srvs = get_value_as_key(server_ips)

    qoe_ts, qoes = getTimeQoE(client_trace, QoE="cascading")
    ax1 = axarr[ctype_ind]

    ax1.plot(qoe_ts, qoes, 'b-', label=control_type)
    minTS = min(min(qoe_ts), min(qoe_ts))
    maxTS = max(max(qoe_ts), max(qoe_ts))
    num_intvls = int((maxTS - minTS)/intvl) + 1
    ts_labels = [minTS + x*intvl for x in range(num_intvls)]
    # str_ts = [datetime.datetime.fromtimestamp(x*intvl + minTS).strftime('%H:%M') for x in range(num_intvls)]
    str_ts = [time.strftime("%H:%M", time.gmtime(x*intvl)) for x in range(num_intvls)]
    plt.setp(ax1, xticks=ts_labels, xticklabels=str_ts,yticks=qoe_labels, yticklabels=str_qoe)
    ax1.set_ylim((0,6))
    ax1.set_title(control_type)
    ax1.set_ylabel("Chunk QoE")
    # ax1.set_xlim((minTS, maxTS))

    ss_events, candidates = getSSEvents(client_trace, ip_srvs)
    print candidates
    print ss_events

    ax2 = ax1.twinx()
    # candidates_num = len(candidates)
    candidates_num = 3
    height = 6/float(candidates_num + 1)
    srv_indices = range(1, candidates_num+1)
    srv_pos = [float(ind) * height for ind in srv_indices]
    for ts in sorted(ss_events.keys(), key=float):
        pre_srv = ss_events[ts]['pre']
        pre_pos = srv_pos[candidates.index(pre_srv)]
        cur_srv = ss_events[ts]['cur']
        cur_pos = srv_pos[candidates.index(cur_srv)]
        # ax2.arrow(ts, pre_pos, 0, cur_pos - pre_pos, fc='r', ec='r')
        ax2.annotate("", xy=(ts, pre_pos), xytext=(ts, cur_pos),arrowprops=dict(arrowstyle="->",fc='r', ec='r'))
    plt.setp(ax2, yticks=srv_pos, yticklabels=fk_srv_names[:candidates_num])
    ax2.set_ylim((0,6))
    ax2.set_ylabel("Candidate Servers")
    ctype_ind += 1

plt.show()
save_fig(fig, imgFolder+"cmp_ss_control_exp", ".all")
