import json
import numpy as np
import pylab
import sys
import ntpath
import matplotlib.pyplot as plt
import glob
import re
import bisect
from matplotlib.backends.backend_pdf import PdfPages

def getSessionQoE(qoeDat):
	chunkID = qoeDat.keys()
	chunkID.sort(key=int)
	if type(qoeDat[chunkID[0]]) == type(dict()):
		chunkQoEs = [qoeDat[k]['QoE'] for k in chunkID]
	else:
		chunkQoEs = [qoeDat[k] for k in chunkID]
	session_qoe = sum(chunkQoEs) / len(chunkQoEs)
	return session_qoe

def draw_cdf(data, ls, lg):
	sorted_data = np.sort(data)
	yvals = np.arange(len(sorted_data))/float(len(sorted_data))

	## Count the percent of session crashes
	gt_zero_ind = bisect.bisect_right(sorted_data, 0)
	gt_zero_percent = yvals[gt_zero_ind]
	print "{0:.0f}%".format(gt_zero_percent * 100), " crashed sessions for method ", lg

	## Count the 80% of user QoE
	gt_tenpercent_ind = bisect.bisect_right(yvals, 0.2)
	gt_tenpercent_qoe = sorted_data[gt_tenpercent_ind]
	print "80-percentile QoE is ", str(gt_tenpercent_qoe), " for method: ", lg

	## Count the 90% of user QoE
	gt_tenpercent_ind = bisect.bisect_right(yvals, 0.1)
	gt_tenpercent_qoe = sorted_data[gt_tenpercent_ind]
	print "90-percentile QoE is ", str(gt_tenpercent_qoe), " for method: ", lg

	## Count the 95% of user QoE
	gt_tenpercent_ind = bisect.bisect_right(yvals, 0.05)
	gt_tenpercent_qoe = sorted_data[gt_tenpercent_ind]
	print "95-percentile QoE is ", str(gt_tenpercent_qoe), " for method: ", lg

	plt.plot(sorted_data, yvals, ls, label=lg, linewidth=2.0)
	# plt.show()

def read_by_suffix(datafolder, suffix):
	qoes = []
	## Get all dash client QoE files
	client_files = glob.glob(datafolder + "*" + suffix)

	for client_file in client_files:
		## Parse DASH Results
		fPath, fName = ntpath.split(client_file)
		client = fName.split('_')[0]
		print "Processing file for client, ", client
		qoeDat = json.load(open(client_file))
		qoe = getSessionQoE(qoeDat)
		qoes.append(qoe)
		print "Session QoE in DASH Client for ", client, ": ", str(qoe)

	return qoes

datafolder = "./dataQoE/type/"

nonSuffix = "_non.json"
cpuSuffix = "_cpu.json"
ioSuffix = "_io.json"
memSuffix = "_mem.json"
bwSuffix = "_bw.json"

non_qoes = read_by_suffix(datafolder, nonSuffix)
cpu_qoes = read_by_suffix(datafolder, cpuSuffix)
mem_qoes = read_by_suffix(datafolder, memSuffix)
io_qoes = read_by_suffix(datafolder, ioSuffix)
bw_qoes = read_by_suffix(datafolder, bwSuffix)

print "Processing ", len(non_qoes), " QoE based methods under non interference!"
print "Processing ", len(cpu_qoes), " QoE based methods under cpu interference!"
print "Processing ", len(mem_qoes), " QoE based methods under memory interference!"
print "Processing ", len(io_qoes), " QoE based methods under io interference!"
print "Processing ", len(bw_qoes), " QoE based methods under bw interference!"

fig, ax = plt.subplots()
draw_cdf(non_qoes, 'k-', 'Non')
draw_cdf(cpu_qoes, 'bo', 'CPU')
draw_cdf(mem_qoes, 'r--', 'Memory')
draw_cdf(io_qoes, 'g-.', 'I/O')
draw_cdf(bw_qoes, 'm-x', 'Bandwidth')
#plt.axhline(y=0.05, xmin=0, xmax=5, linewidth=0.5, color='k', linestyle='--')
#plt.axhline(y=0.1, xmin=0, xmax=5, linewidth=0.5, color='b', linestyle='--')
#plt.axhline(y=0.2, xmin=0, xmax=5, linewidth=0.5, color='r', linestyle='--')
ax.set_xlabel(r'Session QoE', fontsize=20)
ax.set_ylabel(r'The percentage of users', fontsize=20)
ax.set_title('The CDF of user session QoE', fontsize=20)
plt.legend(bbox_to_anchor=(0.35, 0.8))
plt.show()

pdf = PdfPages('./imgs/qoe_cdf_stresstype_cdf.pdf')
pdf.savefig(fig)

pdf.close()

