"""
Demo of scatter plot on porto experiments with QAS-DASH Server switches.
"""
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook

# Load Porto Experiments on QAS_DASH
filePath = "./data/porto/"
dataPreffix = "porto-QAS_DASH-"
dataSuffix = "-BBB.json"
pingPreffix = "porto-"
pingSuffix = "-PING.json"
expNum = 8

def getSSNum(qoeDat):
	ss_num = 0
	chunkID = qoeDat.keys()
	chunkID.sort(key=int)
	sortedServer = [qoeData[k]['Server'] for k in chunkID]
	for i in range(len(sortedServer) - 1):
		curServer = sortedServer[i]
		nextServer = sortedServer[i+1]
		if nextServer != curServer
			ss_num = ss_num + 1

	return ss_num

x = []
y = []
ssNum = []
for i in range(1, 8):
	pingFileName = filePath + pingPreffix + "exp" + str(i) + pingSuffix
	pingDat = json.load(open(pingFileName))

	candidateSrvs = pingDat.keys().sort()
	curX = pingDat[candidateSrvs[0]]
	x.append(curX)
	curY = pingDat[candidateSrvs[1]]
	y.append(curY)

	qoeFileName = filePath + filePreffix + "exp" + str(i) + fileSuffix
	qoeDat = json.load(open(qoeFileName))
	ss_num = getSSNum(qoeDat)
	ssNum.append(ss_num)

# Marker size in units of points^2
volume = 10 * ssNum

fig, ax = plt.subplots()
ax.scatter(x, y, s=volume, alpha=0.5)

ax.set_xlabel(r'RTT to Candidate Server 1', fontsize=20)
ax.set_ylabel(r'RTT to Candidate Server 2', fontsize=20)
ax.set_title('Volume and percent change')

ax.grid(True)
fig.tight_layout()

plt.show()
