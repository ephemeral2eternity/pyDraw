import json
import numpy as np
import pylab
import sys
import matplotlib.pyplot as plt
import glob
import re
from scipy.interpolate import UnivariateSpline
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

def draw_pdf(data, n, ls, lg):
	p, x = np.histogram(data, bins=n)
	x = x[:-1] + (x[1] - x[0])/2
	f = UnivariateSpline(x, p, s=n)
	plt.plot(x, f(x), ls, label=lg, linewidth=2.0)

datafolder = "./data/"

dashQoE = []
dashSuffix = "_DASH_BBB.json"
qasSuffix = "_QAS_BBB.json"
cqasSuffix = "_CQAS_DASH_BBB.json"

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

## Get all dash client QoE files
qasQoE = []
qas_client_files = glob.glob(datafolder + "*" + qasSuffix)

for client_file in qas_client_files:
	## Parse DASH Results
	client = re.search(datafolder + "(.*?)" + qasSuffix, client_file).group(1)
	print "Processing file for client, ", client
	qasDat = json.load(open(client_file))
	qas_qoe = getSessionQoE(qasDat)
	qasQoE.append(qas_qoe)
	print "Session QoE in DASH Client for ", client, ": ", str(qas_qoe)


print "Processing ", len(dash_client_files), " DASH sessions!"
print "Processing ", len(qas_client_files), " QAS-DASH sessions!"

n = 200
fig, ax = plt.subplots()
draw_pdf(dashQoE, n, 'k-', 'DASH')
draw_pdf(qasQoE, n, 'b--', 'QAS-DASH')
ax.set_xlabel(r'Session QoE', fontsize=20)
ax.set_ylabel(r'The number of sessions', fontsize=20)
ax.set_title('The PDF of user session QoE', fontsize=20)
plt.legend(bbox_to_anchor=(0.4, 0.9))
#pylab.ylim([0,1])
#pylab.xlim([0,5])
plt.show()

pdf = PdfPages('./imgs/plc_dashqoe_pdf.pdf')
pdf.savefig(fig)

pdf.close()

