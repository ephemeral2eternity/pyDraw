import numpy as np
import matplotlib.pyplot as plt
import json
import pylab
from matplotlib.backends.backend_pdf import PdfPages

def getCandidates(qoeDat):
	candidates = qoeDat[qoeDat.keys()[0]].keys()
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

qas_dash_srvqoe = json.load(open(dataFolder + "test-exp1-QAS_DASH-BBB-srvqoe.json"))
cqas_dash_srvqoe = json.load(open(dataFolder + "test-exp1-CQAS_DASH-BBB-srvqoe.json"))

chunkid_qas_dash = getChunkID(qas_dash_srvqoe)
candidate_srvs = getCandidates(qas_dash_srvqoe)
print candidate_srvs
qas_srv_qoes = getSrvQoE(qas_dash_srvqoe, candidate_srvs)
chunkid_cqas_dash = getChunkID(cqas_dash_srvqoe)
cqas_srv_qoes = getSrvQoE(cqas_dash_srvqoe, candidate_srvs)

fig,axes = plt.subplots(2,1,sharex=True,sharey=True)
# frame1 = plt.gca()
#for xlabel_i in frame1.axes.get_xticklabels():
#    xlabel_i.set_visible(False)
#    xlabel_i.set_fontsize(20.0)
#for xlabel_i in frame1.axes.get_yticklabels():
#    xlabel_i.set_fontsize(20.0)
#    xlabel_i.set_visible(False)
#for tick in frame1.axes.get_xticklines():
#    tick.set_visible(False)
#for tick in frame1.axes.get_yticklines():
#    tick.set_visible(False)

ax1 = axes[0]
line1 = ax1.plot(chunkid_qas_dash, qas_srv_qoes[candidate_srvs[0]], 'b-', label='Server A')
line2 = ax1.plot(chunkid_qas_dash, qas_srv_qoes[candidate_srvs[1]], 'k:', label='Server B')
plt.setp(line1, linewidth=2.0)
plt.setp(line2, linewidth=3.0)
plt.setp( ax1.get_xticklabels(), visible=False)
ax1.legend(bbox_to_anchor=(1, 0.35))
ax1.set_title('QAS-DASH')
ax1.set_ylim([0,6])

ax2 = axes[1]
line1 = ax2.plot(chunkid_cqas_dash, cqas_srv_qoes[candidate_srvs[0]], 'b-', label='Server A')
line2 = ax2.plot(chunkid_cqas_dash, cqas_srv_qoes[candidate_srvs[1]], 'k:', label='Server B')
plt.setp(line1, linewidth=2.0)
plt.setp(line2, linewidth=3.0)
ax2.legend(bbox_to_anchor=(1, 0.35))

ax2.set_title('CQAS-DASH')
ax2.set_ylim([0,6])

fig.text(0.5, 0.02, 'Chunk No.', ha='center', fontsize=20)
fig.text(0.04, 0.5, 'Server QoE Evalutaions', va='center', rotation='vertical', fontsize=20)
plt.show()

pdf = PdfPages('./imgs/srv_qoes_plot.pdf')
pdf.savefig(fig)

pdf.close()