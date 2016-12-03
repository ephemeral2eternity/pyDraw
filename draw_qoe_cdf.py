import json
import numpy as np
import pylab
import sys
import matplotlib.pyplot as plt
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

# Load Porto Experiments on QAS_DASH
# clients = ['california', 'hongkong', 'iowa', 'japan','singapore', 'netherland', 'ireland', 'texas', 'virginia']
# clients = ['ireland', 'oregon', 'california', 'tokyo','singapore']
# clients = ['ireland']

datafolder = sys.argv[1]
expNum = int(sys.argv[2])

dashQoE = []
qasDashQoE = []
cqasDashQoE = []
dashSuffix = "*DASH_BBB.json"
qasSuffix = "*QAS_DASH_BBB.json"
cqasSuffix = "*CQAS_DASH_BBB.json"

## dash_client_files = 

for client in clients:
	filePath = "./" + datafolder +"/"
	clientPreffix = client + '_'

	for i in range(1, expNum + 1):
		## Parse QAS-DASH Results
		qasFileName = filePath + clientPreffix + "exp" + str(i) + qasSuffix
		qasDat = json.load(open(qasFileName))
		# ssNum.append(ss_num + 1)
		qas_qoe = getSessionQoE(qasDat)
		qasDashQoE.append(qas_qoe)
		print "Session QoE in QAS-DASH for ", client, "in exp", str(i), ": ", str(qas_qoe)

		## Parse DASH Results
		dashFileName = filePath + clientPreffix + "exp" + str(i) + dashSuffix
		dashDat = json.load(open(dashFileName))
		dash_qoe = getSessionQoE(dashDat)
		dashQoE.append(dash_qoe)
		print "Session QoE in DASH for ", client, "in exp", str(i), ": ", str(dash_qoe)

		## Parse CQAS-DASH Results
		cqasFileName = filePath + clientPreffix + "exp" + str(i) + cqasSuffix
		cqasDat = json.load(open(cqasFileName))
		cqas_dash_qoe = getSessionQoE(cqasDat)
		cqasDashQoE.append(cqas_dash_qoe)
		print "Session QoE in CQAS-DASH for ", client, "in exp", str(i), ": ", str(dash_qoe)


fig, ax = plt.subplots()
draw_cdf(dashQoE, 'k-', 'DASH')
draw_cdf(qasDashQoE, 'b-o', 'QAS-DASH')
draw_cdf(cqasDashQoE, 'm-+', 'CQAS-DASH')
ax.set_xlabel(r'Session QoE', fontsize=20)
ax.set_ylabel(r'The percentage of users', fontsize=20)
ax.set_title('The CDF of user session QoE', fontsize=20)
plt.legend(bbox_to_anchor=(1, 0.25))
#pylab.ylim([0,1])
#pylab.xlim([0,5])
plt.show()

pdf = PdfPages('./imgs/cloud_qoe_cdf.pdf')
pdf.savefig(fig)

pdf.close()

