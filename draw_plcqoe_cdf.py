import json
import numpy as np
import pylab
import sys
import matplotlib.pyplot as plt
import glob
import re
from matplotlib.backends.backend_pdf import PdfPages

def getSessionQoE(qoeDat):
	chunkID = qoeDat.keys()
	chunkID.sort(key=int)
	chunkQoEs = [qoeDat[k]['QoE'] for k in chunkID]
	session_qoe = sum(chunkQoEs) / len(chunkQoEs)
	return session_qoe

def draw_cdf(data, ls, lg):
	sorted_data = np.sort(data)
	yvals = np.arange(len(sorted_data))/float(len(sorted_data))
	plt.plot(sorted_data, yvals, ls, label=lg, linewidth=2.0)
	# plt.show()

datafolder = "./data/"

dashQoE = []
dashSuffix = "_DASH_BBB.json"
qasSuffix = "_QAS_BBB.json"
cqasSuffix = "_CQAS_BBB.json"

## Get all dash client QoE files
dash_client_files = glob.glob(datafolder + "*" + dashSuffix)

for client_file in dash_client_files:
	## Parse DASH Results
	client = re.search(datafolder + "(.*?)" + dashSuffix, client_file).group(1)
	print "Processing file for client, ", client
	dashDat = json.load(open(client_file))
	qoe = getSessionQoE(dashDat)
	dashQoE.append(qoe)
	print "Session QoE in DASH Client for ", client, ": ", str(qoe)

## Get all qas_dash client QoE files
qasQoE = []
qasdash_client_files = glob.glob(datafolder + "*" + qasSuffix)

for client_file in qasdash_client_files:
	## Parse DASH Results
	client = re.search(datafolder + "(.*?)" + qasSuffix, client_file).group(1)
	print "Processing file for client, ", client
	qasdashDat = json.load(open(client_file))
	qas_qoe = getSessionQoE(qasdashDat)
	qasQoE.append(qas_qoe)
	print "Session QoE in QAS_DASH Client for ", client, ": ", str(qas_qoe)

## Get all qas_dash client QoE files
cqasQoE = []
cqasdash_client_files = glob.glob(datafolder + "*" + cqasSuffix)

for client_file in cqasdash_client_files:
	## Parse DASH Results
	client = re.search(datafolder + "(.*?)" + cqasSuffix, client_file).group(1)
	print "Processing file for client, ", client
	cqasdashDat = json.load(open(client_file))
	cqas_qoe = getSessionQoE(cqasdashDat)
	cqasQoE.append(cqas_qoe)
	print "Session QoE in CQAS_DASH Client for ", client, ": ", str(cqas_qoe)

print "Processing ", len(dash_client_files), " DASH sessions!"
print "Processing ", len(qasdash_client_files), " QAS sessions!"
print "Processing ", len(cqasdash_client_files), " CQAS sessions!"

fig, ax = plt.subplots()
draw_cdf(dashQoE, 'k-', 'DASH')
draw_cdf(qasQoE, 'b-.', 'QAS-DASH')
draw_cdf(cqasQoE, 'r--', 'CQAS-DASH')
ax.set_xlabel(r'Session QoE', fontsize=20)
ax.set_ylabel(r'The percentage of users', fontsize=20)
ax.set_title('The CDF of user session QoE', fontsize=20)
plt.legend(bbox_to_anchor=(0.35, 0.8))
plt.show()

pdf = PdfPages('./imgs/plc_qoe_cdf.pdf')
pdf.savefig(fig)

pdf.close()

