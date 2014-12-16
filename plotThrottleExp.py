import numpy as np
import matplotlib.pyplot as plt
import json
from matplotlib.backends.backend_pdf import PdfPages


def getChunkQoE(qoeDat):
	chunkID = qoeDat.keys()
	chunkID.sort(key=int)
	chunkQoE = [qoeDat[k]['QoE'] for k in chunkID]
	return chunkQoE

def getChunkID(qoeDat):
	chunkID = qoeDat.keys()
	chunkID.sort(key=int)
	return chunkID

dataFolder = "./data/test/"

data1 = json.load(open(dataFolder + "test1-exp1-DASH-BBB.json"))
data2 = json.load(open(dataFolder + "test2-exp1-QAS_DASH-BBB.json"))
data3 = json.load(open(dataFolder + "test3-exp1-CQAS_DASH-BBB.json"))

chunkid1 = getChunkID(data1)
qoe1 = getChunkQoE(data1)
chunkid2 = getChunkID(data2)
qoe2 = getChunkQoE(data2)
chunkid3 = getChunkID(data3)
qoe3 = getChunkQoE(data3)

# plt.figure(1)
fig, ax = plt.subplots()
line1 = plt.plot(chunkid1, qoe1, 'b-', label='DASH')
line2 = plt.plot(chunkid2, qoe2, 'k--', label='QAS-DASH')
line3 = plt.plot(chunkid3, qoe3, 'm-^', label='CQAS-DASH')
plt.setp(line1, linewidth=2.0)
plt.setp(line2, linewidth=3.0)
plt.setp(line3, linewidth=2.0)
plt.legend(bbox_to_anchor=(1, 0.25))
ax.set_xlabel(r'Chunk No.', fontsize=20)
ax.set_ylabel(r'Chunk QoE Value', fontsize=20)
plt.show()

pdf = PdfPages('./imgs/throttle_qoes.pdf')
pdf.savefig(fig)

pdf.close()