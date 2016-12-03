## Plot client QoE trace over time
# Chen Wang
# plot_client_qoe.py
import json
import numpy as np
import pylab
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def movingaverage(values,window):
    weigths = np.repeat(1.0, window)/window
    #including valid will REQUIRE there to be enough datapoints.
    #for example, if you take out valid, it will start @ point one,
    #not having any prior points, so itll be 1+0+0 = 1 /3 = .3333
    mn_val = sum(values)/float(len(values))
    print mn_val
    extended_values = values
    for i in range(1, window):
    	extended_values.append(mn_val)
    smas = np.convolve(extended_values, weigths, 'valid')
    return smas # as a numpy array

dataFolder = "./dataQoE/failures/http/cmpClients/"

plt_styles = ['k-*', 'b-o', 'g-.', 'm->', 'y-s', 'mp']

dataFiles = {
				'load' : 'crash_pl-node-1.csl.sri.com_03290000_load.json',
				'rtt' : 'crash_plab4.eece.ksu.edu_03290000_rtt.json',
				'hop' : 'crash_pl2.6test.edu.cn_03290000_hop.json',
				'random' : 'crash_pl1.cs.montana.edu_03290000_random.json',
				'qoe' : 'planetlab2.cs.uoregon.edu_03290000_qoe.json'
			}

ls_id = 0
fig, ax = plt.subplots()
for method in dataFiles.keys():
	curFile = dataFolder + dataFiles[method]
	curDat = json.load(open(curFile))
	chunkID = curDat.keys()
	chunkID.sort(key=int)
	chunkQoEs = [curDat[k]['QoE'] for k in chunkID]
	smoothChunkQoE = movingaverage(chunkQoEs, 6)
	print len(chunkQoEs), len(smoothChunkQoE)
	ls = plt_styles[ls_id]
	plt.plot(chunkID, smoothChunkQoE, ls, label=method, linewidth=2.0)
	ls_id = ls_id + 1

ax.set_xlabel(r'Chunk Number', fontsize=20)
ax.set_ylabel(r'Chunk QoE (0-5)', fontsize=20)
# ax.set_title('Moving Average of Chunk QoE with window size = 6', fontsize=20)
#plt.yticks([1, 2, 3, 4, 5], ['Bad', 'Poor', 'Fair', 'Good', 'Excellent'], fontsize=20)
pylab.ylim([0,6])
plt.axvline(x=180, linewidth=1, color='r', linestyle='-')
plt.axvline(x=540, linewidth=1, color='r', linestyle='-')
plt.legend(bbox_to_anchor=(1.1, 0.6), prop={'size':20})

plt.show()

pdf = PdfPages('./imgs/failure_http_client_qoe_curve.pdf')
pdf.savefig(fig)

pdf.close()
