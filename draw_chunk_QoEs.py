# Draw chunk QoEs versus timestamps.
# See correlations between QoE and interference introduced.
# Chen Wang, May 4, 2015
import json
import numpy as np
import pylab
import sys
import matplotlib.pyplot as plt
import glob
import os
import re
import datetime
from matplotlib.backends.backend_pdf import PdfPages

## ===============================================================================================
# Get the timestamp and QoE series from a video session
# @input : qoeDat ----- A json dict storing client trace for one video session
# @return: chunkTS ---- a series of timestamp data
#          QoE ---- a series of Chunk QoE data
## ===============================================================================================
def getChunkQoE(qoeDat):
	chunkID = qoeDat.keys()
	chunkID.sort(key=int)
	chunkQoEs = [qoeDat[k]['QoE'] for k in chunkID]
	chunkTS = [qoeDat[k]['TS'] for k in chunkID]
	return (chunkTS, chunkQoEs)

## ===============================================================================================
# Get the timestamp and response time series from a video session
# @input : qoeDat ----- A json dict storing client trace for one video session
# @return: chunkTS ---- a series of timestamp data
#          rspTimes ---- a series of Chunk response time
## ===============================================================================================
def getChunkRspTime(qoeDat):
	chunkID = qoeDat.keys()
	chunkID.sort(key=int)
	chunkRspTimes = [qoeDat[k]['Response'] for k in chunkID]
	chunkTS = [qoeDat[k]['TS'] for k in chunkID]
	return (chunkTS, chunkRspTimes)

## ===============================================================================================
# Get the timestamp and buffer size series from a video session
# @input : qoeDat ----- A json dict storing client trace for one video session
# @return: chunkTS ---- a series of timestamp data
#          bufStat ---- a series of buffer size data
## ===============================================================================================
def getChunkBufStat(qoeDat):
	chunkID = qoeDat.keys()
	chunkID.sort(key=int)
	chunkBufStat = [qoeDat[k]['Buffer'] for k in chunkID]
	chunkTS = [qoeDat[k]['TS'] for k in chunkID]
	return (chunkTS, chunkBufStat)

## ===============================================================================================
# Get the timestamp and freezing time series from a video session
# @input : qoeDat ----- A json dict storing client trace for one video session
# @return: chunkTS ---- a series of timestamp data
#          freezingTime ---- a series of freezing time data
## ===============================================================================================
def getChunkFreezing(qoeDat):
	chunkID = qoeDat.keys()
	chunkID.sort(key=int)
	chunkFreezingTime = [qoeDat[k]['Freezing'] for k in chunkID]
	chunkTS = [qoeDat[k]['TS'] for k in chunkID]
	return (chunkTS, chunkFreezingTime)

## ===============================================================================================
# Get the bitrate of each chunk in a video session
# @input : qoeDat ----- A json dict storing client trace for one video session
# @return: chunkTS ---- a series of timestamp data
#          bitrate ---- a series of chunk bitrate data
## ===============================================================================================
def getChunkBitrate(qoeDat):
	bitrateReps = { u'1' : 313769, u'2' : 722907, u'3' : 1292014, u'4' : 1917529, u'5' : 2925460, u'6' : 4023268, u'7' : 5477193, u'8' : 8769548, u'9' : 11365148}
	chunkID = qoeDat.keys()
	chunkID.sort(key=int)
	chunkBitrate = [bitrateReps[qoeDat[k]['Representation']] for k in chunkID]
	chunkTS = [qoeDat[k]['TS'] for k in chunkID]
	return (chunkTS, chunkBitrate)

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

dataFolder = './dataQoE/dynamics/bw/vm1/'
dashSuffix = ".json"

#filter_obj = dict(filter_key="Server", filter_value="cache-03")

plt_styles = ['k-', 'b-', 'r-', 'm-', 'y-', 'g-']

## Get all dash client QoE files
dash_client_files = glob.glob(dataFolder + "*" + dashSuffix)

## Filter client names by their locations
client_filter = ['ricepl-1', 'ricepl-2', 'ricepl-5']

## Draw all chunk QoEs versus the timestampes
clientNum = 0
filtered_clients = []
fig, ax = plt.subplots()
minTS = None
maxTS = None
for client_file in dash_client_files:
	## Parse DASH Results
	client = re.search(dataFolder + "(.*?)" + dashSuffix, client_file).group(1)
	print "Processing file for client, ", client
	for cfilter in client_filter:
		if cfilter in client:
			dashDat = json.load(open(client_file))
			# if get_filtered_vals(dashDat, filter_obj):
			filtered_clients.append(client)
			
			ts, qoes = getChunkQoE(dashDat)
			plt.plot(ts, qoes, plt_styles[client_filter.index(cfilter)])
			clientNum = clientNum + 1
			if minTS is None:
				minTS = min(ts)
			else:
				minTS = min(minTS, min(ts))
			if maxTS is None:
				maxTS = max(ts)
			else:
				maxTS = max(maxTS, max(ts))

## Change the time stamp ticks
num_intvs = int((maxTS - minTS)/300) + 1
ts_labels = [minTS + x*300 for x in range(num_intvs)]
str_ts = [datetime.datetime.fromtimestamp(x*300 + minTS).strftime('%H:%M') for x in range(num_intvs)]
plt.xticks(ts_labels, str_ts, fontsize=15)

ax.set_xlabel("Time", fontsize=20)
ax.set_ylabel("Chunk Response Time(secondes)", fontsize=20)

plt.ylim((0,5))
plt.xlim((minTS, minTS + 600))
plt.show()


#print "There are totally ", str(clientNum), " connecting to the server ", filter_obj['filter_value']
#print "These clients are: "
#print filtered_clients

pdf = PdfPages('./imgs/chunk_qoe_rice_bw_pstress.pdf')
pdf.savefig(fig)

pdf.close()