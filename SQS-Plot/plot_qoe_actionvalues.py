# Plot QoE action value for one server on all cache agents
# Chen Wang
# chenw@andrew.cmu.edu
# plot_qoe_actionvalues.py
import json
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def plot_qoe_on_agents(dataFolder, cache_agents, ts, srv, tsInterval):
	qoe_files = {}
	for agent in cache_agents:
		qoe_files[agent] = dataFolder + agent+ "_" + ts + "_QoE.json"

	plt_styles = ['k-v', 'b-8', 'r-x', 'm->', 'y-s', 'k-h', 'g-^', 'b-o', 'r-*', 'm-d', 'y-<', 'g-o']

	figNo = 0
	fig, ax = plt.subplots()
	for agent in qoe_files.keys():
		print "Ploting QoE evaluation on agent:", agent
		srv_tr = json.load(open(qoe_files[agent]))
		srv_tr_to_plot = srv_tr[srv]
		plt_ts = [int(x) for x in srv_tr_to_plot.keys() if int(x) > tsInterval[0] and int(x) < tsInterval[1]]
		sorted_ts = sorted(plt_ts)
		tr_vals = [srv_tr_to_plot[str(cur_ts)] for cur_ts in sorted_ts]
		agentName = '$S_{' + str(int(agent.split('-')[1])) + '}$'
		plt.plot(sorted_ts, tr_vals, plt_styles[figNo], label=agentName, linewidth=2.0, markersize=8)
		figNo = figNo + 1

	## Change the time stamp ticks
	num_intvs = int((tsInterval[1] - tsInterval[0])/900) + 1
	ts_labels = [tsInterval[0] + x*900 for x in range(num_intvs)]
	str_ts = [datetime.datetime.fromtimestamp(x*900 + tsInterval[0]).strftime('%H:%M') for x in range(num_intvs)]
	plt.xticks(ts_labels, str_ts, fontsize=15)

	box = ax.get_position()
	# ax.set_position([box.x0, box.y0 + 0.1, box.width, box.height * 0.9])
	ax.legend(bbox_to_anchor=(1.15, 0.9),
		          fancybox=True, shadow=True, ncol=3, prop={'size':20})
	params = {'legend.fontsize': 15,
	          'legend.linewidth': 2}
	plt.rcParams.update(params)
	# ax.set_title('Server QoE Score for crashed server at various agents.', fontsize=20)
	ax.set_xlabel("Time in a day", fontsize=20)
	ax.set_ylabel("Server QoE Score (0-5)", fontsize=20)
	# ax.set_ylim([0,5])
	plt.show()

	print srv
	print ts

	pdf = PdfPages('./imgs/' + srv + '_' + ts +'_qoe_on_agents.pdf')
	pdf.savefig(fig)
	pdf.close()


dataFolder = "./srvQoE/failures/http/"
cache_agents = ["cache-01", "cache-02", "cache-03", "cache-04", "cache-05", "cache-06", "cache-07", "cache-08", "cache-09", "cache-10", "cache-11", "cache-12"]
ts = "03290500"
srv = "cache-08"
tsInterval = [1427587200, 1427590800]
plot_qoe_on_agents(dataFolder, cache_agents, ts, srv, tsInterval)

