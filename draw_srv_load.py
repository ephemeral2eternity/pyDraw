# Plot Server Load during various streaming session
# Chen Wang
# chenw@andrew.cmu.edu
# draw_srv_load.py
import json
import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

## ==================================================================================
# Get the average server load within a time interval
# @input : load_file ----- The server load file name
#		   intvls ---- The time interval to compute the average server load
# @return: the average server load within the time interval
## ==================================================================================
def get_srv_load_intvl_mean(load_file, intvls):
	load_tr = json.load(open(load_file))
	ts = [int(x) for x in load_tr.keys() if int(x) > intvls[0] and int(x) < intvls[1]]
	sorted_ts = sorted(ts)
	load_vals = [int(load_tr[str(cur_ts)]) for cur_ts in sorted_ts]

	intvl_mean_load = sum(load_vals) / float(len(load_vals))
	return intvl_mean_load

## ==================================================================================
# Draw the bar graph of all servers load during a period a certain method is running.
# @input : dataFolder ----- The folder of load data files.
#		   cache_agents ---- The servers to draw the server load
#		   methods ---- The various methods to draw
#		   TS ---- The file name timestamp for various methods (A dictionary with 
#					method name as keys)
#		   tsIntervals ----- The time interval of each method running period.
## ==================================================================================
def draw_srv_load(dataFolder, cache_agents, methods, TS, tsIntervals):
	hatches = ['*', '/', '.', '\\', 'o', '+', 'x', '0']
	colors = ['r', 'y', 'b', 'm', 'g', 'c', '#eeefff', '#a2a7ff']

	N = len(cache_agents)
	ind = np.arange(N)			# The x locations for the groups
	width = 0.15 				# The width of the bars

	srv_loads = {}

	fig = plt.figure()
	ax = fig.add_subplot(111)

	bar_count = 0
	for method in methods:
		srv_loads[method] = {}
		loads = []
		load_usrs = []
		for agent in cache_agents:
			load_file = dataFolder + agent + "_" + TS[method] + "_load.json"
			srv_loads[method][agent] = get_srv_load_intvl_mean(load_file, tsIntervals[method])
			loads.append(srv_loads[method][agent])
			load_usrs.append(srv_loads[method][agent] / float(5.0*12))

		cur_ind = [x + bar_count*width for x in ind]
		ax.bar(cur_ind, loads, width, label=method, color=colors[bar_count], hatch=hatches[bar_count])
		bar_count = bar_count + 1

		mn_load = sum(loads) / float(len(loads))
		std_load = (sum((x-mn_load)**2 for x in loads))**0.5
		print "Method: ", method, ": The mean load is ", str(mn_load), " and the std of the load among servers are : ", str(std_load)

		mn_load_usr = sum(load_usrs) / float(len(load_usrs))
		std_load_usr = (sum((x-mn_load_usr)**2 for x in load_usrs))**0.5
		print "Method: ", method, ": The mean user load is ", str(mn_load_usr), " and the std of the user load among servers are : ", str(std_load_usr)

	tick_ind = [x + bar_count*width/2 for x in ind]
	plt.xticks(tick_ind, cache_agents, fontsize=15)

	box = ax.get_position()
	ax.set_position([box.x0, box.y0 + 0.1, box.width, box.height * 0.9])
	ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.25),
		          fancybox=True, shadow=True, ncol=5)

	params = {'legend.fontsize': 15,
	          'legend.linewidth': 2}
	plt.rcParams.update(params)
	ax.set_title('Average Server Load in Various Methods (# of chunk requests / 5 minutes)', fontsize=15)

	ax.set_xlabel("Cache Servers")
	ax.set_ylabel("Load (# of chunk requests / 5 minutes)")
	plt.show()

	pdf = PdfPages('./imgs/srv_load_cache04_vmcrash.pdf')
	pdf.savefig(fig)
	pdf.close()


## Compare server load for cache-06 cpu stressed case
dataFolder = "./srvQoE/"
methods = ["load", "rtt", "hop", "random", "qoe"]
# methods = ["load", "rtt", "hop", "random"]
cache_agents = ["cache-01", "cache-02", "cache-03", "cache-05", "cache-06", "cache-07", "cache-08", "cache-09", "cache-10", "cache-11", "cache-12"]
TS = {
		"load" : "03090500",
		"rtt" : "03090500",
		"hop" : "03090500",
		"random" : "03090500",
		"qoe" : "03091200"
		}

tsIntervals = {
				"load" : [1425865200, 1425865800],
				"rtt" : [1425866400, 1425867000],
				"hop" : [1425868200, 1425868800],
				"random" : [1425870000, 1425870600],
				"qoe" : [1425900600, 1425901200]
				}

draw_srv_load(dataFolder, cache_agents, methods, TS, tsIntervals)



