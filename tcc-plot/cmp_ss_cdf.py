import json
import numpy as np
import pylab
import sys
import matplotlib.pyplot as plt
import glob
import re
from loadData.loadSS import *
from rstPlots.draw_cdf import *
from rstPlots.save_fig import *
from matplotlib.backends.backend_pdf import PdfPages

plt_styles = ['k-', 'b--', 'r-.', 'm-', 'y-', 'g-']
intvl = 60
dataFolder = 'D://GitHub/pyDraw/tcc-data/control-exps/'
imgFolder = 'D://GitHub/pyDraw/tcc-imgs/'

client_control_suffix = "1000_client_cascading_exp_greedy.json"
server_control_suffix = "1030_server_qoe_cascading_exp_greedy.json"
dash_suffix = "1100_dash_rtt.json"

client_control_files = glob.glob(dataFolder + "*" + client_control_suffix)
server_control_files = glob.glob(dataFolder + "*" + server_control_suffix)
dash_files = glob.glob(dataFolder + "*" + dash_suffix)

client_control_ss = loadAllSSNum(client_control_files)
server_control_ss = loadAllSSNum(server_control_files)
dash_ss = loadAllSSNum(dash_files)

percentile = 0.9
fig, ax = plt.subplots()
# dash_percentile_ss = draw_cdf(ax, dash_ss, plt_styles[0], "DASH Client with \nRTT based Server Selection", percentile)
client_percentile_ss = draw_cdf(ax, client_control_ss, plt_styles[1], "Client-side Control", percentile)
server_percentile_ss = draw_cdf(ax, server_control_ss, plt_styles[2], "Server-side Control", percentile)

ax.set_xlabel(r'Number of Server Switches per Session', fontsize=15)
ax.set_ylabel(r'The percentage of users', fontsize=15)
ax.set_title('The CDF of Server Switches in a Streaming Session', fontsize=15)
#plt.axhline(y=1-percentile, linewidth=0.5, xmin=0, xmax=5, color='g', linestyle='--')
#ax.annotate("QoE:" + "{:.2f}".format(dash_percentile_qoe), xy=(dash_percentile_qoe, 1-percentile), xytext=(dash_percentile_qoe, 1-percentile+0.2), color="black",
#            arrowprops=dict(facecolor="black", edgecolor="black", width=1))
#ax.annotate("QoE:" + "{:.2f}".format(client_percentile_qoe), xy=(client_percentile_qoe, 1-percentile), xytext=(client_percentile_qoe+0.2, 1-percentile+0.25), color="blue",
#            arrowprops=dict(facecolor="blue", edgecolor="blue", width=1))
#ax.annotate("QoE:" + "{:.2f}".format(server_percentile_qoe), xy=(server_percentile_qoe, 1-percentile), xytext=(server_percentile_qoe+0.6, 1-percentile+0.05), color="red",
#            arrowprops=dict(facecolor="red", edgecolor="red", width=1))

#plt.text(3, 0.11, '90th percentile QoE', color='g')
plt.legend(loc=4,fontsize=15)
save_fig(fig, imgFolder+"control_exp_sscdf", ".all")
plt.show()