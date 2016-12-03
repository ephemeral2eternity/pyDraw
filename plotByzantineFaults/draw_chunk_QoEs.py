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
# Get the response time of each chunk in a video session
# @input : qoeDat ----- A json dict storing client trace for one video session
# @return: chunkTS ---- a series of timestamp data
#          rspTimes ---- a series of chunk response times
## ===============================================================================================
def getChunkRspTime(qoeDat):
	chunkID = qoeDat.keys()
	chunkID.sort(key=int)
	rspTimes = [float(qoeDat[k]['Response']) for k in chunkID]
	chunkTS = [qoeDat[k]['TS'] for k in chunkID]
	return (chunkTS, rspTimes)

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