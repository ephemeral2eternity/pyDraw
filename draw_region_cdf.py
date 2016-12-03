import json
import numpy as np
import sys
import glob
import re
import operator
import pylab
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def getSessionQoE(qoeDat):
        chunkID = qoeDat.keys()
        chunkID.sort(key=int)
        chunkQoEs = [qoeDat[k]['QoE'] for k in chunkID]
        session_qoe = sum(chunkQoEs) / len(chunkQoEs)
        return session_qoe

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

def draw_cdf(data, ls, lg):
        sorted_data = np.sort(data)
        yvals = np.arange(len(sorted_data))/float(len(sorted_data))
        plt.plot(sorted_data, yvals, ls, label=lg, linewidth=2.0)
        # plt.show()

region = sys.argv[1]
datafolder = "./info/"
closestSuffix = "_CLOSEST.json"

## Get all client closest json files
client_closest_files = glob.glob(datafolder + "*" + closestSuffix)

## Read files and save closest server, zone and region to following dicts
closest_srvs = {}
closest_zones = {}
closest_regions = {}

## Read files for every client
for cl_file in client_closest_files:
		## Parse Closest Server, Zone, and Region
		cl_closest = json.load(open(cl_file))
		# Get Client Name
		client = re.search(datafolder + "(.*?)" + closestSuffix, cl_file).group(1)
		#print "Processing file for client, ", client

		clst_srv = cl_closest['Server']
		clst_zone = cl_closest['Zone']
		clst_region = cl_closest['Region']

		## Add the client to the closest_srvs dict
		if clst_srv not in closest_srvs.keys():
			closest_srvs[clst_srv] = []
		closest_srvs[clst_srv].append(client)

		## Add the client to the cloest_zone dict
		if clst_zone not in closest_zones.keys():
			closest_zones[clst_zone] = []
		closest_zones[clst_zone].append(client)

		## Add the client to the cloest_regions dict
		if clst_region not in closest_regions.keys():
			closest_regions[clst_region] = []
		closest_regions[clst_region].append(client)

europe_clients = closest_regions[region]
# print europe_clients
qoe_folder = "./zone_exps/"
dashSuffix = "_exp4_BBB.json"
## Inter-zone server selection suffixes
qasSuffix = "_exp2_QAS_BBB.json"
cqasSuffix = "_exp2_CQAS_BBB.json"

## Get all dash client QoE files
dash_client_files = glob.glob(qoe_folder + "exp4/*" + dashSuffix)
dash_file_num = 0
dashQoE = []
for client_file in dash_client_files:
        ## Parse DASH Results
        client = re.search(qoe_folder + "exp4/"+ "(.*?)" + dashSuffix, client_file).group(1)
	# print client
	if client in europe_clients:
        	print "Client, ", client, " is in the region of europe, process the client file!"
        	dashDat = json.load(open(client_file))
        	qoe = getSessionQoE(dashDat)
        	dashQoE.append(qoe)
        	print "Session QoE in DASH Client for ", client, ": ", str(qoe)
		dash_file_num = dash_file_num + 1

## Get all qas_dash client QoE files
qasQoE = []
qasdash_client_files = glob.glob(qoe_folder +"exp2/*" + qasSuffix)
qas_dash_file_num = 0
for client_file in qasdash_client_files:
        ## Parse DASH Results
        client = re.search(qoe_folder + "exp2/" + "(.*?)" + qasSuffix, client_file).group(1)
	if client in europe_clients:
        	print "Client, ", client, " is in the region of europe, process the client file!"
        	qasdashDat = json.load(open(client_file))
        	qas_qoe = getSessionQoE(qasdashDat)
        	qasQoE.append(qas_qoe)
        	print "Session QoE in QAS_DASH Client for ", client, ": ", str(qas_qoe)
		qas_dash_file_num = qas_dash_file_num + 1

## Get all qas_dash client QoE files
cqasQoE = []
cqasdash_client_files = glob.glob(qoe_folder + "exp2/*" + cqasSuffix)
cqas_dash_file_num = 0
for client_file in cqasdash_client_files:
        ## Parse DASH Results
        client = re.search(qoe_folder + "exp2/" + "(.*?)" + cqasSuffix, client_file).group(1)
	if client in europe_clients:
        	print "Client, ", client, " is in the region of europe, process the client file!"
        	cqasdashDat = json.load(open(client_file))
        	cqas_qoe = getSessionQoE(cqasdashDat)
        	cqasQoE.append(cqas_qoe)
		print "Session QoE in CQAS_DASH Client for ", client, ": ", str(cqas_qoe)
		cqas_dash_file_num = cqas_dash_file_num + 1

print "Processing ", dash_file_num, " DASH sessions!"
print "Processing ", qas_dash_file_num, " QAS sessions!"
print "Processing ", cqas_dash_file_num, " CQAS sessions!"

fig, ax = plt.subplots()
draw_cdf(dashQoE, 'k-', 'DASH')
draw_cdf(qasQoE, 'b-.', 'Inter-zone QAS-DASH')
draw_cdf(cqasQoE, 'r--', 'Inter-zone CQAS-DASH')
ax.set_xlabel(r'Session QoE', fontsize=20)
ax.set_ylabel(r'The percentage of users', fontsize=20)
ax.set_title('The CDF of user session QoE in ' + region, fontsize=20)
plt.legend(bbox_to_anchor=(0.45, 0.8))
plt.show()

pdf = PdfPages('./imgs/plc_' + region + '_cdf.pdf')
pdf.savefig(fig)

pdf.close()

## Count the SLA satisfaction
sla_qoe = 4.0
dash_satisfaction = get_satisfaction(dashQoE, sla_qoe)
print "The DASH SLA satisfaction in region", region, "is: ", dash_satisfaction
qas_satisfaction = get_satisfaction(qasQoE, sla_qoe)
print "The QAS-DASH SLA satisfaction in region", region, "is: ", qas_satisfaction
cqas_satisfaction = get_satisfaction(cqasQoE, sla_qoe)
print "The CQAS-DASH SLA satisfaction in region", region, "is : ", cqas_satisfaction
