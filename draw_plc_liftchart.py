import json
import numpy as np
import pylab
import sys
import ntpath
import matplotlib.pyplot as plt
import glob
import re
from matplotlib.backends.backend_pdf import PdfPages

def getSessionQoE(qoeDat):
	chunkID = qoeDat.keys()
	chunkID.sort(key=int)
	if type(qoeDat[chunkID[0]]) == type(dict()):
		chunkQoEs = [qoeDat[k]['QoE'] for k in chunkID]
	else:
		chunkQoEs = [qoeDat[k] for k in chunkID]
	session_qoe = sum(chunkQoEs) / len(chunkQoEs)
	return session_qoe

## ===============================================================================================
# Draw the lift chart of the QoE data
## ===============================================================================================
def draw_lift_chart(data, ls, lg):
	sorted_data = np.sort(data)
	xvals = np.arange(len(sorted_data))/float(len(sorted_data))
	plt.plot(xvals, sorted_data, ls, label=lg, linewidth=2.0)

	ind = np.arange(10)/10.0

	ind_str = ["{0:.0f}%".format(x * 100) for x in ind]
	plt.xticks(ind, ind_str, fontsize=15)
	# plt.show()

def read_by_suffix(datafolder, suffix):
	qoes = []
	## Get all dash client QoE files
	client_files = glob.glob(datafolder + "*" + suffix)

	for client_file in client_files:
		## Parse DASH Results
		fPath, fName = ntpath.split(client_file)
		client = fName.split('_')[0]
		# print "Processing file for client, ", client
		qoeDat = json.load(open(client_file))
		qoe = getSessionQoE(qoeDat)
		qoes.append(qoe)
		print "Session QoE in DASH Client for ", client, ": ", str(qoe)

	return qoes

datafolder = "./dataQoE_cache-01_cpustress/cpu_stress/"

qoeSuffix = "_qoe.json"
loadSuffix = "_load.json"
rttSuffix = "_rtt.json"
hopSuffix = "_hop.json"
randomSuffix = "_random.json"

qoe_qoes = read_by_suffix(datafolder, qoeSuffix)
load_qoes = read_by_suffix(datafolder, loadSuffix)
rtt_qoes = read_by_suffix(datafolder, rttSuffix)
hop_qoes = read_by_suffix(datafolder, hopSuffix)
random_qoes = read_by_suffix(datafolder, randomSuffix)

print "Processing ", len(qoe_qoes), " QoE based server selection streaming sessions!"
print "Processing ", len(load_qoes), " load based server selection streaming sessions!"
print "Processing ", len(rtt_qoes), " rtt based server selection streaming sessions!"
print "Processing ", len(hop_qoes), " hop based server selection streaming sessions!"
print "Processing ", len(random_qoes), " random server selection streaming sessions!"

fig, ax = plt.subplots()
draw_lift_chart(qoe_qoes, 'k-', 'QoE')
draw_lift_chart(load_qoes, 'b-o', 'Load')
draw_lift_chart(rtt_qoes, 'r--', 'RTT')
draw_lift_chart(hop_qoes, 'g-.', 'Hop Number')
draw_lift_chart(random_qoes, 'y-+', 'Random')
ax.set_xlabel(r'User Percentile', fontsize=20)
ax.set_ylabel(r'Session QoE (0-5) ', fontsize=20)
ax.set_title('The gain chart of streaming session QoE', fontsize=20)
# ax.set_xlim([0, 0.1])
plt.legend(bbox_to_anchor=(0.8, 0.4))
plt.show()

pdf = PdfPages('./imgs/method_cmp_gainchart_cache-01_cpustress.pdf')
pdf.savefig(fig)

pdf.close()

