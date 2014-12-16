"""
Demo of scatter plot on porto experiments with QAS-DASH Server switches.
"""
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
from matplotlib.backends.backend_pdf import PdfPages

def getSSNum(qoeDat):
	ss_num = 0
	chunkID = qoeDat.keys()
	chunkID.sort(key=int)
	sortedServer = [qoeDat[k]['Server'] for k in chunkID]
	for i in range(len(sortedServer) - 1):
		curServer = sortedServer[i]
		nextServer = sortedServer[i+1]
		if nextServer != curServer:
			ss_num = ss_num + 1

	return ss_num

def getSessionQoE(qoeDat):
	chunkID = qoeDat.keys()
	chunkID.sort(key=int)
	chunkQoEs = [qoeDat[k]['QoE'] for k in chunkID]
	session_qoe = sum(chunkQoEs) / len(chunkQoEs)
	return session_qoe


def square(a):
	return [i**2 for i in a]


# Load Porto Experiments on QAS_DASH
clients = ['netherland', 'ireland', 'virginia', 'iowa','texas', 'california', 'hongkong', 'singapore', 'japan']
# clients = ['ireland']
x = []
y = []
ssNum = []
qoeRatio = []
dashSuffix = "-DASH-BBB.json"
qasSuffix = "-QAS_DASH-BBB.json"
cqasSuffix = "-CQAS_DASH-BBB.json"
pingSuffix = "-PING.json"

for client in clients:
	filePath = "./data/" + client + '/'
	clientPreffix = client + '_'

	expNum = 6

	for i in range(1, expNum + 1):
		pingFileName = filePath + clientPreffix + "exp" + str(i) + pingSuffix
		pingDat = json.load(open(pingFileName))

		candidateSrvs = pingDat.keys()
		candidateSrvs.sort()
		curX = pingDat[candidateSrvs[0]]
		print "candidate server 1: ", str(curX)
		x.append(curX)
		curY = pingDat[candidateSrvs[1]]
		print "candidate server 2: ", str(curY)
		y.append(curY)

		## Parse QAS-DASH Results
		qasFileName = filePath + clientPreffix + "exp" + str(i) + qasSuffix
		qasDat = json.load(open(qasFileName))
		ss_num = getSSNum(qasDat)
		print "Server switches in QAS-DASH for ", client, "in exp", str(i), ": ", str(ss_num)
		# ssNum.append(ss_num + 1)
		qas_qoe = getSessionQoE(qasDat)
		print "Session QoE in QAS-DASH for ", client, "in exp", str(i), ": ", str(qas_qoe)

		## Parse QAS-DASH Results
		cqasFileName = filePath + clientPreffix + "exp" + str(i) + cqasSuffix
		cqasDat = json.load(open(cqasFileName))
		ss_cqas_num = getSSNum(cqasDat)
		print "Server switches in CQAS-DASH for ", client, "in exp", str(i), ": ", str(ss_num)
		ssNum.append(ss_cqas_num + 1)
		cqas_qoe = getSessionQoE(cqasDat)
		print "Session QoE in CQAS-DASH for ", client, "in exp", str(i), ": ", str(cqas_qoe)

		## Parse DASH Results
		dashFileName = filePath + clientPreffix + "exp" + str(i) + dashSuffix
		dashDat = json.load(open(dashFileName))
		dash_qoe = getSessionQoE(dashDat)
		print "Session QoE in DASH for ", client, "in exp", str(i), ": ", str(dash_qoe)

		## Compute improvement of QoE in QAS-DASH over DASH
		qas_qoe_ratio = qas_qoe / dash_qoe
		# qas_qoe_ratio = cqas_qoe / dash_qoe
		# print "CQAS-DASH improves QoE with ratio: ", str(qas_qoe_ratio)
		print "QAS-DASH improves QoE with ratio: ", str(qas_qoe_ratio)
		qoeRatio.append(qas_qoe_ratio)


# Marker size in units of points^2
# volume1 = 30 * square(ssNum)
org = 1
scl = 50
qoe_improve = [(q - org)*scl for q in qoeRatio]
print qoe_improve
min_qoe_improve = min(qoe_improve)
print "Minimum QoE improvement is: ", str(min_qoe_improve)
volume_q = [(q - min_qoe_improve) for q in qoe_improve]
volume = square(square(volume_q))


fig2, ax2 = plt.subplots()
ax2.scatter(x, y, s=volume, alpha=0.5)

ax2.set_xlabel(r'RTT to Candidate Server 1', fontsize=20)
ax2.set_ylabel(r'RTT to Candidate Server 2', fontsize=20)
ax2.set_title('QoE Improvement in QAS-DASH', fontsize=20)

ax2.grid(True)
fig2.tight_layout()

plt.show()

pdf = PdfPages('./imgs/qoe_improve_scatter.pdf')
pdf.savefig(fig2)

pdf.close()
