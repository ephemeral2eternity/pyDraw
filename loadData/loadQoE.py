# Draw chunk QoEs versus timestamps.
# See correlations between QoE and interference introduced.
# Chen Wang, Feb. 19, 2016
import os
import json

## ===============================================================================================
# Get the timestamp and QoE series from a video session
# @input : qoeDat ----- A json dict storing client trace for one video session
# @return: chunkTS ---- a series of timestamp data
#          QoE ---- a series of Chunk QoE data
## ===============================================================================================
def getTimeQoE(clientTrace, QoE="cascading"):
    chunkID = clientTrace.keys()
    chunkID.sort(key=int)
    if QoE == "linear":
        qoe_model = "QoE1"
    else:
        qoe_model = "QoE2"
    chunkQoEs = [clientTrace[k][qoe_model] for k in chunkID]
    chunkTS = [clientTrace[k]['TS'] for k in chunkID]
    return (chunkTS, chunkQoEs)

## ===============================================================================================
# Get the timestamp and corresponding chunk bitrates from a trace file for a video session
# @input : qoeDat ----- A json dict storing client trace for one video session
# @return: chunkTS ---- a series of timestamp data
#          chunkBitrates ---- a series of Chunk bitrate level data
## ===============================================================================================
def getTimeBitrate(clientTrace):
    chunkID = clientTrace.keys()
    chunkID.sort(key=int)
    chunkBitrates = [int(clientTrace[k]["Representation"]) for k in chunkID]
    chunkTS = [clientTrace[k]['TS'] for k in chunkID]
    return (chunkTS, chunkBitrates)

## ===============================================================================================
# Get the session QoE from a streaming session tracefile
# @input : qoeDat ----- A json dict storing client trace for one video session
# @return: session_qoe ---- an average of all chunk qoes in a video streaming session
## ===============================================================================================
def getSessionQoE(qoeDat, QoE="cascading"):
    chunkID = qoeDat.keys()
    chunkID.sort(key=int)
    if QoE == "linear":
        qoe_model = "QoE1"
    else:
        qoe_model = "QoE2"
    chunkQoEs = [qoeDat[k][qoe_model] for k in chunkID]
    session_qoe = sum(chunkQoEs) / len(chunkQoEs)
    return session_qoe

## ===============================================================================================
# Get the session QoE from a streaming session tracefile
# @input : qoeDat ----- A json dict storing client trace for one video session
# @return: session_qoe ---- an average of all chunk qoes in a video streaming session
## ===============================================================================================
def loadAllSessionQoE(file_list, QoE="cascading"):
    session_qoes = []
    for client_file in file_list:
        ## Parse DASH Results
        client_file_name = os.path.basename(client_file)
        client = client_file_name.split('_')[0]
        print "Processing file for client, ", client
        dashDat = json.load(open(client_file))
        qoe = getSessionQoE(dashDat, QoE)
        session_qoes.append(qoe)
        print "Session QoE in DASH Client for ", client, ": ", str(qoe)
    return session_qoes


def loadSQS(SQS_trace):
    tses = SQS_trace.keys()
    tses.sort(key=float)
    ts_data = [float(ts) for ts in tses]
    candidate_servers = SQS_trace[tses[0]].keys()

    sqs_data = {}
    for srv in candidate_servers:
        sqs_data[srv] = []

    for ts in tses:
        for srv in candidate_servers:
            sqs_data[srv].append(SQS_trace[ts][srv])

    return (ts_data, candidate_servers, sqs_data)
