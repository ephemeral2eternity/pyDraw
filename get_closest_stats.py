import json
import numpy
import sys
import glob
import re
import operator

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

## Count stats in each server, zone and region
closest_srv_num = {}
closest_zone_num = {}
closest_region_num = {}

## Obtain counts of each dict
for key in closest_srvs:
	closest_srv_num[key] = len(closest_srvs[key])
#print closest_srv_num

for key in closest_zones:
	closest_zone_num[key] = len(closest_zones[key])
#print closest_zone_num

for key in closest_regions:
	closest_region_num[key] = len(closest_regions[key])
#print closest_region_num

##print "============================================================="
sorted_region = sorted(closest_region_num.items(), key=operator.itemgetter(1), reverse=True)
top_region = sorted_region[0][0]
top_region_nodes = closest_regions[top_region]

for node in top_region_nodes:
	print node
##print "============================================================="
