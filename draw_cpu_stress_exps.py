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

def get_percentile(data, percent):
	data_len = len(data)
	sorted_data = sorted(data, reverse=True)
	idx = int(data_len * percent)
	return sorted_data[idx]

def get_satisfaction(data, qoe_lv):
	data_num = len(data)
	satisfactory_data = [d for d in data if d > qoe_lv]
	satisfactory = len(satisfactory_data) / float(len(data))
	return satisfactory

datafolder = "./stress-exps/"

exp_prefixes = ['nostress', 'cpu8', 'cpu16']
plt_styles = ['k-', 'b-.', 'r:', 'm--', 'y-s', 'k-+', 'g-^', 'b-o', 'r-*', 'm-d']

dashSuffix = "_stress_BBB.json"

exp_qoes = {}

for exp in exp_prefixes:
	exp_folder = datafolder + exp + '/'

	## Get all dash client QoE files
	dash_client_files = glob.glob(exp_folder + "*" + dashSuffix)
	dashQoE = []

	for client_file in dash_client_files:
		## Parse DASH Results
		client = re.search(datafolder + "(.*?)" + dashSuffix, client_file).group(1)
		print "Processing file for client, ", client
		dashDat = json.load(open(client_file))
		qoe = getSessionQoE(dashDat)
		dashQoE.append(qoe)
		print "Session QoE in DASH Client for ", client, ": ", str(qoe)

	exp_qoes[exp] = dashQoE

sty_id = 0
mnQoE = []
qoe90 = []
qoe80 = []
vio4 = []
vio4_5 = []
exp_names = []
fig, ax = plt.subplots()
for key in sorted(exp_qoes):
	draw_cdf(exp_qoes[key], plt_styles[sty_id], 'stress lvl = ' + key)
	sty_id = sty_id + 1
	mnQoE.append(sum(exp_qoes[key]) / float(len(exp_qoes[key])))
	exp_names.append(key)
	qoe90.append(get_percentile(exp_qoes[key], 0.9))
	qoe80.append(get_percentile(exp_qoes[key], 0.8))
	vio4.append(get_satisfaction(exp_qoes[key], 4))
	vio4_5.append(get_satisfaction(exp_qoes[key], 4.5))

ax.set_xlabel(r'Session QoE', fontsize=20)
ax.set_ylabel(r'The percentage of users', fontsize=20)
ax.set_title('The CDF of user session QoE', fontsize=20)
plt.legend(bbox_to_anchor=(0.45, 0.9))
plt.show()

pdf = PdfPages('./imgs/cpu_stress_cdf.pdf')
pdf.savefig(fig)
pdf.close()

fig, ax = plt.subplots()
plt.plot(range(len(exp_names)), mnQoE, 'k-', label="Mean Session QoEs", linewidth=2.0)
plt.plot(range(len(exp_names)), qoe90, 'b--', label="90-percentile Session QoE", linewidth=2.0)
plt.plot(range(len(exp_names)), qoe80, 'r:', label="80-percentile Session QoE", linewidth=2.0)
ax.set_xlabel(r'The stress level', fontsize=20)
ax.set_ylabel(r'The average session QoE', fontsize=20)
plt.xticks(range(len(exp_names)), exp_names, fontsize=15)
ax.set_title('The average session QoE for in CPU-Stressed Experiment', fontsize=20)
plt.legend(bbox_to_anchor=(0.6, 0.9))
plt.show()

pdf = PdfPages('./imgs/cpu_stress_mnqoe.pdf')
pdf.savefig(fig)
pdf.close()

fig, ax = plt.subplots()
plt.plot(range(len(exp_names)), vio4, 'k-', label="Satisfactory QoE = 4", linewidth=2.0)
plt.plot(range(len(exp_names)), vio4_5, 'b--', label="Satisfactory QoE = 4.5", linewidth=2.0)
ax.set_xlabel(r'The stress level', fontsize=15)
plt.xticks(range(len(exp_names)), exp_names, fontsize=15)
ax.set_ylabel(r'The percent of clients meeting satisfactory QoE', fontsize=15)
ax.set_title('QoE Satisfaction', fontsize=20)
plt.legend(bbox_to_anchor=(0.6, 0.9))
plt.show()

pdf = PdfPages('./imgs/cpu_stress_satisfaction.pdf')
pdf.savefig(fig)
pdf.close()
