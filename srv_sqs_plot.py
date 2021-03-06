import numpy as np
import matplotlib.pyplot as plt
import json
from matplotlib.backends.backend_pdf import PdfPages

def getCandidates(qoeDat):
	candidates = qoeDat[qoeDat.keys()[0]]
	return candidates

def getSrvQoE(qoeDat, candidates):
	chunkID = qoeDat.keys()
	chunkID.sort(key=int)
	srv_qoes = {}
	for c in candidates:
		srv_qoe = [qoeDat[k][c] for k in chunkID]
		srv_qoes[c] = srv_qoe
	return srv_qoes

def getChunkID(qoeDat):
	chunkID = qoeDat.keys()
	chunkID.sort(key=int)
	return chunkID

dataFolder = "./data/test/"

qas_dash_srvqoe = json.load(open(dataFolder + "test1-exp1-QAS_DASH-BBB-srvqoe.json"))
cqas_dash_srvqoe = json.load(open(dataFolder + "test2-exp1-CQAS_DASH-BBB-srvqoe.json"))

chunkid_qas_dash = getChunkID(qas_dash_srvqoe)
candidate_srvs = getCandidates(qoeDat)
qas_srv_qoes = getSrvQoE(qoeDat, candidate_srvs)
chunkid_cqas_dash = getChunkID(cqas_dash_srvqoe)
cqas_srv_qoes = getSrvQoE(cqas_dash_srvqoe, candidate_srvs)

plt.figure(1)
ax = plt.subplot(211)
line1 = plt.plot(chunkid_qas_dash, qas_srv_qoes[candidates[0]], 'b-', label=candidates[0])
line2 = plt.plot(chunkid_qas_dash, qas_srv_qoes[candidates[1]], 'k--', label=candidates[1])
plt.setp(line1, linewidth=2.0)
plt.setp(line2, linewidth=3.0)
plt.legend(bbox_to_anchor=(1, 0.25))
ax.set_xlabel(r'Chunk No.', fontsize=20)
ax.set_ylabel(r'QoE Evaluations on Candidate Servers', fontsize=20)
ax.title(r'QAS-DASH Server Evaluations')

ax = plt.subplot(212)
line1 = plt.plot(chunkid_cqas_dash, cqas_srv_qoes[candidates[0]], 'b-', label=candidates[0])
line2 = plt.plot(chunkid_cqas_dash, cqas_srv_qoes[candidates[1]], 'k--', label=candidates[1])
plt.setp(line1, linewidth=2.0)
plt.setp(line2, linewidth=3.0)
plt.legend(bbox_to_anchor=(1, 0.25))
ax.set_xlabel(r'Chunk No.', fontsize=20)
ax.set_ylabel(r'QoE Evaluations on Candidate Servers', fontsize=20)
ax.title(r'CQAS-DASH Server Evaluations')
plt.show()

pdf = PdfPages('./imgs/srv_qoes_plot.pdf')
pdf.savefig(fig)

pdf.close()