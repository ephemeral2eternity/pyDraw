import numpy as np
import matplotlib.pyplot as plt
import pylab
import json
from matplotlib.backends.backend_pdf import PdfPages


def getChunkServer(qoeDat):
	chunkID = qoeDat.keys()
	chunkID.sort(key=int)
	chunkServer = [qoeDat[k]['Server'] for k in chunkID]
	return chunkServer

def getChunkID(qoeDat):
	chunkID = qoeDat.keys()
	chunkID.sort(key=int)
	return chunkID

def get_srv_data(server1, candidates):
	srv_data = []
	for srv in server1:
		cur_srv_idx = candidates.index(srv) + 1
		srv_data.append(cur_srv_idx)
	return srv_data

dataFolder = "./data/test/"
candidates = ['agens-01', 'agens-02']

data1 = json.load(open(dataFolder + "test-exp1-DASH-BBB.json"))
data2 = json.load(open(dataFolder + "test-exp1-QAS_DASH-BBB.json"))
data3 = json.load(open(dataFolder + "test-exp1-CQAS_DASH-BBB.json"))


chunkid1 = getChunkID(data1)
server1 = getChunkServer(data1)
srv_data1 = get_srv_data(server1, candidates)

chunkid2 = getChunkID(data2)
server2 = getChunkServer(data2)
srv_data2 = get_srv_data(server2, candidates)
chunkid3 = getChunkID(data3)
server3 = getChunkServer(data3)
srv_data3 = get_srv_data(server3, candidates)

fig =  plt.figure()
ax1 = plt.subplot(311)
line1 = plt.plot(chunkid1, srv_data1, 'b+', label='DASH')
#ax1.set_xlabel(r'Chunk No.')
#ax1.set_ylabel(r'Selected Server')
plt.yticks([1, 2], ['Server A', 'Server B'], fontsize=20)
pylab.ylim([0,3])
plt.legend()
ax2 = plt.subplot(312)
line2 = plt.plot(chunkid2, srv_data2, 'ks', label='QAS-DASH')
#ax2.set_xlabel(r'Chunk No.')
#ax2.set_ylabel(r'Selected Server')
plt.yticks([1, 2], ['Server A', 'Server B'], fontsize=20)
pylab.ylim([0,3])
plt.legend(bbox_to_anchor=(1, 0.4))
ax3 = plt.subplot(313)
line3 = plt.plot(chunkid3, srv_data3, 'm-', label='CQAS-DASH')
ax3.set_xlabel(r'Chunk No.', fontsize=20)
# ax3.set_ylabel(r'Selected Server', fontsize=20)
plt.yticks([1, 2], ['Server A', 'Server B'], fontsize=20)
pylab.ylim([0,3])
plt.legend()
plt.show()

pdf = PdfPages('./imgs/ssplot.pdf')
pdf.savefig(fig)

pdf.close()

#pdf = PdfPages('./imgs/throttle_qoes.pdf')
#pdf.savefig(fig)

#pdf.close()