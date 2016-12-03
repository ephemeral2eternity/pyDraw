# Draw user CDF filtered by certain field
# Chen Wang
# chenw@andrew.cmu.edu
# draw_filtered_qoe_cdf.py

import json
import numpy as np
import pylab
import sys
import ntpath
import matplotlib.pyplot as plt
import glob
import re
from matplotlib.backends.backend_pdf import PdfPages

## ===============================================================================================
# Draw the cdf of QoE data
## ===============================================================================================
def draw_cdf(data, ls, lg):
	sorted_data = np.sort(data)
	yvals = np.arange(len(sorted_data))/float(len(sorted_data))
	plt.plot(sorted_data, yvals, ls, label=lg, linewidth=2.0)
	# plt.show()

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

## ===============================================================================================
# Return the session QoE from client QoE trace
## ===============================================================================================
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
# Check if the client QoE Data contains filter_obj["filter_value"] in its filter_obj["filter_key"]
# @input : qoeDat ----- A json dict storing client traces
#		   filter_obj ---- A dict to denote the key and value to be filtered. Keys of the object are:
#							"filter_key" : denotes the key to filter in client trace (can be ,
#											"Buffer", "Freezing", "QoE", "Representation", "Response", 
#											"Server", "TS")
#							"filter_value" : the value to be included in qoeDat
#							It is usually used to filter users connecting to a certain server.
# @return: True ---- the client QoE trace is what is needed
#          False ---- the client QoE trace is not what is looking for
## ===============================================================================================
def get_filtered_vals(qoeDat, filter_obj):
	filtered_values = []
	for ts in qoeDat.keys():
		# print qoeDat[ts]
		# print filter_obj['filter_key']
		if type(qoeDat[ts]) == type(dict()):
			filtered_values.append(qoeDat[ts][filter_obj['filter_key']])
		else:
			return False

	if filter_obj["filter_value"] in filtered_values:
		return True
	else:
		return False

def filter_read_by_suffix(datafolder, suffix, filter_obj):
	qoes = []
	## Get all dash client QoE files
	client_files = glob.glob(datafolder + "*" + suffix)

	for client_file in client_files:
		## Parse DASH Results
		fPath, fName = ntpath.split(client_file)
		client = fName.split('_')[0]
		# print "Processing file for client, ", client
		qoeDat = json.load(open(client_file))

		if get_filtered_vals(qoeDat, filter_obj):
			print "Processing file for client, ", fName
			qoe = getSessionQoE(qoeDat)
			qoes.append(qoe)
			# print "Session QoE in DASH Client for ", client, ": ", str(qoe)

	return qoes

datafolder = "./dataQoE/failures/http/"

qoeSuffix = "_qoe.json"
loadSuffix = "_load.json"
rttSuffix = "_rtt.json"
hopSuffix = "_hop.json"
randomSuffix = "_random.json"

filter_obj = dict(filter_key="Server", filter_value="cache-08")

qoe_qoes = filter_read_by_suffix(datafolder, qoeSuffix, filter_obj)
load_qoes = filter_read_by_suffix(datafolder, loadSuffix, filter_obj)
rtt_qoes = filter_read_by_suffix(datafolder, rttSuffix, filter_obj)
hop_qoes = filter_read_by_suffix(datafolder, hopSuffix, filter_obj)
random_qoes = filter_read_by_suffix(datafolder, randomSuffix, filter_obj)

print "Processing ", len(qoe_qoes), " QoE based server selection streaming sessions!"
print "Processing ", len(load_qoes), " load based server selection streaming sessions!"
print "Processing ", len(rtt_qoes), " rtt based server selection streaming sessions!"
print "Processing ", len(hop_qoes), " hop based server selection streaming sessions!"
print "Processing ", len(random_qoes), " random server selection streaming sessions!"

fig, ax = plt.subplots()
draw_cdf(qoe_qoes, 'k-', 'QoE')
draw_cdf(load_qoes, 'b-o', 'Load')
draw_cdf(rtt_qoes, 'r--', 'RTT')
draw_cdf(hop_qoes, 'g-.', 'Hop Number')
draw_cdf(random_qoes, 'y-+', 'Random')
ax.set_xlabel(r'User Session QoE', fontsize=20)
ax.set_ylabel(r'Percentage of users', fontsize=20)
ax.set_title('The CDF of user session QoE filtered by ' + filter_obj["filter_value"], fontsize=20)
plt.legend(bbox_to_anchor=(0.9, 0.4))
plt.show()

pdf = PdfPages('./imgs/http_failure_qoe_cdf_filtered_by_' + filter_obj["filter_key"] + '_' + filter_obj["filter_value"] + '.pdf')
pdf.savefig(fig)

pdf.close()

