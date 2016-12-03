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

def get_satisfaction(data, qoe_lv):
        data_num = len(data)
        satisfactory_data = [d for d in data if d > qoe_lv]
        satisfactory = len(satisfactory_data) / float(len(data))
        return satisfactory

def draw_cdf(data, ls, lg):
	sorted_data = np.sort(data)
	yvals = np.arange(len(sorted_data))/float(len(sorted_data))
	plt.plot(sorted_data, yvals, ls, label=lg, linewidth=2.0)
	# plt.show()

datafolder = "./zone_exps/"

dashSuffix = "_exp4_BBB.json"
## Inter-zone server selection suffixes
iz_qasSuffix = "_exp5_QAS_BBB.json"
iz_cqasSuffix = "_exp5_CQAS_BBB.json"

## Get all dash client QoE files
dash_client_files = glob.glob(datafolder + "exp4/*" + dashSuffix)

dashQoE = []
for client_file in dash_client_files:
	## Parse DASH Results
	client = re.search(datafolder + "(.*?)" + dashSuffix, client_file).group(1)
	print "Processing file for client, ", client
	dashDat = json.load(open(client_file))
	qoe = getSessionQoE(dashDat)
	dashQoE.append(qoe)
	print "Session QoE in DASH Client for ", client, ": ", str(qoe)

## Get all qas_dash client QoE files
iz_qasQoE = []
iz_qasdash_client_files = glob.glob(datafolder + "exp5/*" + iz_qasSuffix)

for client_file in iz_qasdash_client_files:
	## Parse DASH Results
	client = re.search(datafolder + "(.*?)" + iz_qasSuffix, client_file).group(1)
	print "Processing file for client, ", client
	iz_qasdashDat = json.load(open(client_file))
	iz_qas_qoe = getSessionQoE(iz_qasdashDat)
	iz_qasQoE.append(iz_qas_qoe)
	print "Session QoE in QAS_DASH Client for ", client, ": ", str(iz_qas_qoe)

## Get all qas_dash client QoE files
iz_cqasQoE = []
iz_cqasdash_client_files = glob.glob(datafolder + "exp5/*" + iz_cqasSuffix)

for client_file in iz_cqasdash_client_files:
	## Parse DASH Results
	client = re.search(datafolder + "(.*?)" + iz_cqasSuffix, client_file).group(1)
	print "Processing file for client, ", client
	iz_cqasdashDat = json.load(open(client_file))
	iz_cqas_qoe = getSessionQoE(iz_cqasdashDat)
	iz_cqasQoE.append(iz_cqas_qoe)
	print "Session QoE in CQAS_DASH Client for ", client, ": ", str(iz_cqas_qoe)

print "Processing ", len(dash_client_files), " DASH sessions!"
print "Processing ", len(iz_qasdash_client_files), " Inter-Zone QAS sessions!"
print "Processing ", len(iz_cqasdash_client_files), " Inter-Zone CQAS sessions!"

fig, ax = plt.subplots()
draw_cdf(dashQoE, 'k-', 'DASH')
draw_cdf(iz_qasQoE, 'b-.', 'Inter-Zone QAS-DASH')
draw_cdf(iz_cqasQoE, 'r--', 'Inter-Zone CQAS-DASH')
ax.set_xlabel(r'Session QoE', fontsize=20)
ax.set_ylabel(r'The percentage of users', fontsize=20)
ax.set_title('The CDF of user session QoE', fontsize=20)
plt.legend(bbox_to_anchor=(0.55, 0.9))
plt.show()

pdf = PdfPages('./imgs/node300_bw_throttle_cdf.pdf')
pdf.savefig(fig)

pdf.close()

sla_qoe = 4.0

dash_satisfactory = get_satisfaction(dashQoE, sla_qoe)
print "DASH SLA Satisfaction: ", dash_satisfactory
qas_satisfactory = get_satisfaction(iz_qasQoE, sla_qoe)
print "QAS_DASH SLA Satisfaction: ", qas_satisfactory
cqas_satisfactory = get_satisfaction(iz_cqasQoE, sla_qoe)
print "CQAS_DASH SLA Satisfaction: ", cqas_satisfactory

