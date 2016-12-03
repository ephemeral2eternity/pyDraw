## Compare the QoE and server load with and without CPU stress.
# Chen Wang
# chenw@andrew.cmu.edu
# draw_filtered_qoe_cdf.py

import json
import numpy as np
import pylab
import sys
import ntpath
import matplotlib.pyplot as plt
import glob
import re
from matplotlib.backends.backend_pdf import PdfPages

## ===============================================================================================
# Draw the lift chart of the QoE data
## ===============================================================================================
def draw_lift_chart(data, ls, lg):
	sorted_data = np.sort(data)
	xvals = np.arange(len(sorted_data))/float(len(sorted_data))
	plt.plot(xvals, sorted_data, ls, label=lg, linewidth=2.0)

	ind = np.arange(10)/10.0

	ind_str = ["{0:.0f}%".format(x * 100) for x in ind]
	plt.xticks(ind, ind_str, fontsize=15)

	# plt.show()

## ===============================================================================================
# Return the session QoE from client QoE trace
## ===============================================================================================
def getSessionQoE(qoeDat):
	chunkID = qoeDat.keys()
	chunkID.sort(key=int)
	if type(qoeDat[chunkID[0]]) == type(dict()):
		chunkQoEs = [qoeDat[k]['QoE'] for k in chunkID]
	else:
		chunkQoEs = [qoeDat[k] for k in chunkID]
	session_qoe = sum(chunkQoEs) / len(chunkQoEs)
	return session_qoe

## ===============================================================================================
# Check if the client QoE Data contains filter_obj["filter_value"] in its filter_obj["filter_key"]
# @input : qoeDat ----- A json dict storing client traces
#		   filter_obj ---- A dict to denote the key and value to be filtered. Keys of the object are:
#							"filter_key" : denotes the key to filter in client trace (can be ,
#											"Buffer", "Freezing", "QoE", "Representation", "Response", 
#											"Server", "TS")
#							"filter_value" : the value to be included in qoeDat
#							It is usually used to filter users connecting to a certain server.
# @return: True ---- the client QoE trace is what is needed
#          False ---- the client QoE trace is not what is looking for
## ===============================================================================================
def get_filtered_vals(qoeDat, filter_obj):
	filtered_values = []
	for ts in qoeDat.keys():
		# print qoeDat[ts]
		# print filter_obj['filter_key']
		if type(qoeDat[ts]) == type(dict()):
			filtered_values.append(qoeDat[ts][filter_obj['filter_key']])
		else:
			return False

	if filter_obj["filter_value"] in filtered_values:
		return True
	else:
		return False

## ===============================================================================================
# Read all session qoe from users filtered by certain criterion
# @input : qoeDat ----- A json dict storing client traces
#		   filter_obj ---- A dict to denote the key and value to be filtered. Keys of the object are:
#							"filter_key" : denotes the key to filter in client trace (can be ,
#											"Buffer", "Freezing", "QoE", "Representation", "Response", 
#											"Server", "TS")
#							"filter_value" : the value to be included in qoeDat
#							It is usually used to filter users connecting to a certain server.
# @return: True ---- the client QoE trace is what is needed
#          False ---- the client QoE trace is not what is looking for
## ===============================================================================================
def filter_read_by_suffix(datafolder, suffix, filter_obj):
	qoes = []
	## Get all dash client QoE files
	client_files = glob.glob(datafolder + "*" + suffix)

	for client_file in client_files:
		## Parse DASH Results
		fPath, fName = ntpath.split(client_file)
		client = fName.split('_')[0]
		# print "Processing file for client, ", client
		qoeDat = json.load(open(client_file))

		if get_filtered_vals(qoeDat, filter_obj):
			qoe = getSessionQoE(qoeDat)
			qoes.append(qoe)
			# print "Session QoE in DASH Client for ", client, ": ", str(qoe)

	return qoes

## ===============================================================================================
# Compare qoe lift chart for anomaly server (all users connecting to the srv) with or without anomaly
# @input : datafolder ---- The folder storing data
#		   cmp_srvs ----- Servers to be compared
#		   method ---- The method client is running
## ===============================================================================================
def srv_anomaly_qoe_liftchart(datafolder, observe_srv, method, anormaly_name):
	plt_styles = ['k-', 'b-.', 'r:', 'm--', 'y-s', 'k-+', 'g-^', 'b-o', 'r-*', 'm-d']
	cmp_srv_qoes = {}
	cmp_srv_load = {}

	filter_obj = dict(filter_key="Server", filter_value=observe_srv)
	filesuffix = '_' + method + '.json'
	srv_qoes = filter_read_by_suffix(datafolder + '/' + anormaly_name + '/', filesuffix, filter_obj)
	cmp_srv_qoes[anormaly_name] = srv_qoes

	srv_qoes = filter_read_by_suffix(datafolder + '/normal/', filesuffix, filter_obj)
	cmp_srv_qoes['normal'] = srv_qoes

	fig, ax = plt.subplots()
	plt_count = 0

	for key in cmp_srv_qoes:
		print "Processing ", len(cmp_srv_qoes[key]), " streaming sessions in ", key, "!"
		cmp_srv_load[key] = len(cmp_srv_qoes[key])
		draw_lift_chart(cmp_srv_qoes[key], plt_styles[plt_count], key)
		plt_count = plt_count + 1

	ax.set_xlabel(r'User Percentile', fontsize=20)
	ax.set_ylabel(r'Session QoE', fontsize=20)
	ax.set_title('Compare users\' QoE lift curve with server ' + observe_srv + " with and without " + anormaly_name + " using method " + method, fontsize=20)
	plt.legend(bbox_to_anchor=(0.85, 0.4))
	plt.show()

	pdf = PdfPages('./imgs/anormaly_cmp_liftcurve_' + method + '_' + anormaly_name + '.pdf')
	pdf.savefig(fig)
	pdf.close()
	return cmp_srv_load

## ===============================================================================================
# Compare servers by the number of streaming sessions downloading videos from each server
# @input : srv_load ---- The dictionary storing the number of streaming sessions for each server.
#						The key is the server name, the value is the number of streaming sessions
#		   method ---- The method client is running
## ===============================================================================================
def cmp_srv_load(srv_load, observe_srv, observe_key):
	hatches = ["/" , "\\" , "|" , "-" , "+" , "x", "o", "O", ".", "*" ]
	colors = ['r', 'y', 'b', 'm', 'g', 'c', '#eeefff', '#a2a7ff', '#ffe7ba', '#B97A97']

	methods = srv_load.keys()
	N = len(methods)
	ind = np.arange(N)			# The x locations for the groups
	width = 0.8 / float(len(srv_load[methods[0]].keys()))

	fig, ax = plt.subplots()

	key_id = 0
	for keyword in srv_load[methods[0]].keys():
		cur_method_load = []
		for method in methods:
			cur_method_load.append(srv_load[method][keyword])
		cur_ind = [x + width*key_id for x in ind]
		if keyword == observe_key:
			ax.bar(cur_ind, cur_method_load, width, label=keyword, color=colors[key_id], hatch=hatches[key_id])
		else:
			ax.bar(cur_ind, cur_method_load, width, label=keyword, alpha=0.3, color=colors[key_id], hatch=hatches[key_id])
		key_id = key_id + 1
	
	plt_inds = [x + key_id*width/2.0 for x in ind]
	plt.xticks(plt_inds, methods, fontsize=15)
	ax.set_title('The number of sessions streamed from ' + observe_srv + " with or without " + observe_key, fontsize=15)

	ax.legend(bbox_to_anchor=(0.85, 0.85))

	params = {'legend.fontsize': 15,
	          'legend.linewidth': 2}
	plt.rcParams.update(params)

	ax.set_xlabel("Cache Servers")
	ax.set_ylabel("The number of streaming sessions")
	plt.show()

	pdf = PdfPages('./imgs/anormaly_load_cmp_' + observe_key + '.pdf')
	pdf.savefig(fig)
	pdf.close()

## =================================================================================================
# datafolder = "./dataQoE/"
datafolder = "./dataQoE_cache-01_cpustress/"

methods = ["qoe", "load", "rtt", "hop", "random"]
# methods = ["load"]
observe_srv = "cache-01"
anormaly_name = "cpu_stress"

srv_load = {}
for method in methods:
	method_srv_load = srv_anomaly_qoe_liftchart(datafolder, observe_srv, method, anormaly_name)
	srv_load[method] = method_srv_load

cmp_srv_load(srv_load, observe_srv, anormaly_name)

