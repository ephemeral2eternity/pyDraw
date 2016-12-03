## Plot client QoE trace over time
# Chen Wang
# plot_client_server_selection.py
import json
import numpy as np
import pylab
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

dataFolder = "./dataQoE/failures/http/cmpClients/"

plt_styles = ['k-*', 'b-o', 'g-.', 'm->', 'y-s', 'mp']

dataFile = 'planetlab2.cs.uoregon.edu_03290000_qoe.json'

ls_id = 0
method = "qoe"
fig, ax = plt.subplots()
curFile = dataFolder + dataFile
curDat = json.load(open(curFile))
chunkID = curDat.keys()
chunkID.sort(key=int)
chunkSrvs = [curDat[k]['Server'] for k in chunkID]
ls = plt_styles[ls_id]
chunkSrvVal = [int(srv.split('-')[1]) for srv in chunkSrvs]
plt.plot(chunkID, chunkSrvVal, ls, label=method, linewidth=2.0)

ax.set_xlabel(r'Chunk Number', fontsize=20)
ax.set_ylabel(r'Chunk Server (1-12)', fontsize=20)
# ax.set_title('Selected server for chunk in QoE based client', fontsize=20)
plt.yticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], ['$S_1$', '$S_2$', '$S_3$', '$S_4$', '$S_5$', '$S_6$', '$S_7$', '$S_8$', '$S_9$', '$S_{10}$', '$S_{11}$', '$S_{12}$'], fontsize=20)
pylab.ylim([0,13])
plt.axvline(x=180, linewidth=1, color='r', linestyle='-')
plt.axvline(x=540, linewidth=1, color='r', linestyle='-')
# plt.legend(bbox_to_anchor=(1, 0.55))

plt.show()

pdf = PdfPages('./imgs/failure_http_client_srv_curve.pdf')
pdf.savefig(fig)

pdf.close()
