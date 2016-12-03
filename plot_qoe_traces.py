# Draw QoE evaluation traces on one cache agent
# Chen Wang
# chenw@andrew.cmu.edu
# plot_qoe_traces.py
import json
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def convert_dict_type(srv_tr, trace_type):
	new_srv_tr = {}
	first_tr = srv_tr[srv_tr.keys()[0]]
	if trace_type == 'rtts':
		for srv in first_tr.keys():
			new_srv_tr[srv] = {}

		for srv in new_srv_tr.keys():
			for ts in srv_tr.keys():
				new_srv_tr[srv][ts] = srv_tr[ts][srv]

	return new_srv_tr


def plotTraces(dataFolder, cache_agent, trace_type, TS, tsInterval):
	srv_file = cache_agent + "_" + TS + "_" + trace_type + ".json"
	srv_tr = json.load(open(dataFolder + srv_file))

	if trace_type == 'rtts':
		srv_tr = convert_dict_type(srv_tr, 'rtts')

	plt_styles = ['m-d', 'k-', 'r-x', 'm-+', 'y-s', 'm.', 'g-^', 'b-o', 'r-*','k-.', 'g-.', 'b-', 'k-h',  'm--']

	figNo = 0
	fig, ax = plt.subplots()
	for srv in srv_tr.keys():
		print "Ploting QoE evaluation for server :", srv
		cur_srv_tr = srv_tr[srv]
		ts = [int(x) for x in cur_srv_tr.keys() if int(x) > tsInterval[0] and int(x) < tsInterval[1]]
		sorted_ts = sorted(ts)
		tr_vals = [cur_srv_tr[str(cur_ts)] for cur_ts in sorted_ts]

		srvName = '$S_{' + str(int(srv.split('-')[1])) + '}$'
		plt.plot(sorted_ts, tr_vals, plt_styles[figNo], label=srvName, linewidth=2.0, markersize=8)
		figNo = figNo + 1

	## Change the time stamp ticks
	num_intvs = int((tsInterval[1] - tsInterval[0])/900) + 1
	ts_labels = [tsInterval[0] + x*900 for x in range(num_intvs)]
	str_ts = [datetime.datetime.fromtimestamp(x*900 + tsInterval[0]).strftime('%H:%M') for x in range(num_intvs)]
	plt.xticks(ts_labels, str_ts, fontsize=15)

	box = ax.get_position()
	ax.set_position([box.x0, box.y0 + 0.25, box.width, box.height * 0.75])
	ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.55),
		          fancybox=True, shadow=True, ncol=4, prop={'size':20})
	#params = {'legend.fontsize': 20,
	#          'legend.linewidth': 2}
	#plt.rcParams.update(params)
	# ax.set_title('Server QoE Score Observed on $S_{10}$', fontsize=20)
	# ax.set_xlabel("Time in a day", fontsize=20)
	ax.set_ylabel("Server QoE Score(0-5)", fontsize=20)
	# ax.set_ylim([0,5])
	plt.show()

	pdf = PdfPages('./imgs/' + cache_agent + '_' + trace_type + '_tr.pdf')
	pdf.savefig(fig)
	pdf.close()



dataFolder = "./srvQoE/failures/http/"
trace_type = "QoE"
cache_agent = "cache-10"
TS = "03290500"
tsInterval = [1427587200, 1427590800]
plotTraces(dataFolder, cache_agent, trace_type, TS, tsInterval)
