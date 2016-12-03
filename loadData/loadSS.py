import json
import os

def getSSNum(qoeDat):
    ss_num = 0
    chunkID = qoeDat.keys()
    chunkID.sort(key=int)
    sortedServer = [qoeDat[k]['Server'] for k in chunkID]
    for i in range(len(sortedServer) - 1):
        curServer = sortedServer[i]
        nextServer = sortedServer[i+1]
        if nextServer != curServer:
            ss_num = ss_num + 1

    return ss_num


## ===============================================================================================
# Get the session QoE from a streaming session tracefile
# @input : qoeDat ----- A json dict storing client trace for one video session
# @return: session_qoe ---- an average of all chunk qoes in a video streaming session
## ===============================================================================================
def loadAllSSNum(file_list):
    session_ss_num = []
    for client_file in file_list:
        ## Parse DASH Results
        client_file_name = os.path.basename(client_file)
        client = client_file_name.split('_')[0]
        print "Processing file for client, ", client
        dashDat = json.load(open(client_file))
        ss_num = getSSNum(dashDat)
        session_ss_num.append(ss_num)
        print "The number of server switches in for ", client, ": ", str(ss_num)
    return session_ss_num


## ===============================================================================================
# Get the session QoE from a streaming session tracefile
# @input : qoeDat ----- A json dict storing client trace for one video session
# @return: session_qoe ---- an average of all chunk qoes in a video streaming session
## ===============================================================================================
def getSSEvents(client_trace, ip_to_srvs):
    events = {}
    candidates = []
    chunk_ids = sorted(client_trace.keys(), key=int)
    pre_server_ip = client_trace[chunk_ids[0]]['Server']
    pre_server = ip_to_srvs[pre_server_ip]
    if pre_server not in candidates:
        candidates.append(pre_server)
    for chk_id in chunk_ids[1:]:
        cur_srv_ip = client_trace[chk_id]['Server']
        cur_server = ip_to_srvs[cur_srv_ip]
        curTS = client_trace[chk_id]['TS']
        if cur_server != pre_server:
            events[curTS] = {"pre" : pre_server, "cur" : cur_server}
        if pre_server not in candidates:
            candidates.append(pre_server)
        pre_server = cur_server

    return events, candidates
