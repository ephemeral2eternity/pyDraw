# Draw Server QoE during various periods running different methods
# Chen Wang
# chenw@andrew.cmu.edu
# draw_srv_mn_qoe.py
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
def get_srv_qoe_intvl_mean(qoes_file, agent, intvls):
	srv_qoes = json.load(open(qoes_file))
	if agent in srv_qoes.keys():
		ts = [int(x) for x in srv_qoes[agent].keys() if int(x) > intvls[0] and int(x) < intvls[1]]
		if len(ts) == 0:
			return -1
		sorted_ts = sorted(ts)
		qoe_vals = [int(srv_qoes[agent][str(cur_ts)]) for cur_ts in sorted_ts]

		intvl_mean_qoe = sum(qoe_vals) / float(len(qoe_vals))
		return intvl_mean_qoe
	else:
		return -1

## ==================================================================================
# Draw the bar graph of all servers load during a period a certain method is running.
# @input : dataFolder ----- The folder of load data files.
#		   cache_agents ---- The servers to draw the server load
#		   methods ---- The various methods to draw
#		   TS ---- The file name timestamp for various methods (A dictionary with 
#					method name as keys)
#		   tsIntervals ----- The time interval of each method running period.
## ==================================================================================
def draw_srv_mn_qoe(dataFolder, observe_agent, cache_agents, methods, TS, tsIntervals):
	hatches = ['*', '/', '.', '\\', 'o', '+', 'x', '0']
	colors = ['r', 'y', 'b', 'm', 'g', 'c', '#eeefff', '#a2a7ff']

	N = len(cache_agents)
	ind = np.arange(N)			# The x locations for the groups
	width = 0.15 				# The width of the bars

	srv_qoes = {}

	fig = plt.figure()
	ax = fig.add_subplot(111)

	bar_count = 0
	for method in methods:
		srv_qoes[method] = {}
		qoes = []

		for agent in cache_agents:
			qoes_file = dataFolder + agent + "_" + TS[method] + "_qoe.json"
			srv_qoes[method][agent] = get_srv_qoe_intvl_mean(qoes_file, observe_agent, tsIntervals[method])
			qoes.append(srv_qoes[method][agent])

		cur_ind = [x + bar_count*width for x in ind]
		ax.bar(cur_ind, qoes, width, label=method, color=colors[bar_count], hatch=hatches[bar_count])
		bar_count = bar_count + 1

	tick_ind = [x + bar_count*width/2 for x in ind]
	plt.xticks(tick_ind, cache_agents, fontsize=15)

	box = ax.get_position()
	ax.set_position([box.x0, box.y0 + 0.1, box.width, box.height * 0.9])
	ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.25),
		          fancybox=True, shadow=True, ncol=5)

	params = {'legend.fontsize': 15,
	          'legend.linewidth': 2}
	plt.rcParams.update(params)
	ax.set_title('Average Server QoE Action Value in ' + observe_agent + 'in Various Methods', fontsize=15)

	ax.set_xlabel("Cache Servers")
	ax.set_ylabel("Average QoE Action Value (Averaged for 1 hour running)")
	plt.show()

	pdf = PdfPages('./imgs/' + observe_agent + '_qoe_actionvalue_method_cmp.pdf')
	pdf.savefig(fig)
	pdf.close()


## Compare server load for cache-06 cpu stressed case
dataFolder = "./srvQoE/"
methods = ["load", "rtt", "hop", "random", "qoe"]
observe_agent = "cache-06"
cache_agents = ["cache-01", "cache-02", "cache-03", "cache-04", "cache-05", "cache-06", "cache-07", "cache-08", "cache-09", "cache-10"]
TS = {
		"load" : "03030500",
		"rtt" : "03030500",
		"hop" : "03030500",
		"random" : "03031400",
		"qoe" : "03031400"
		}

tsIntervals = {
				"load" : [1425337200, 1425340800],
				"rtt" : [1425344400, 1425348000],
				"hop" : [1425351600, 1425355200],
				"random" : [1425358800, 1425362400],
				"qoe" : [1425366000, 1425369600]
				}

draw_srv_mn_qoe(dataFolder, observe_agent, cache_agents, methods, TS, tsIntervals)



