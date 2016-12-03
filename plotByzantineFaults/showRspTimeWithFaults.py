## Draw the chunk response time over time for multiple clients
# Compare clients' response time under dynamic server capacity.
# Show client's response time the byzantine faults server have impacted.
# showQoEwithFaults.py
from draw_chunk_QoEs import *

dataFolder = '/Users/Chen/Box Sync/Proposal/Chen\'s Proposal/exps/byzantineFaults/by_type2_0824/'
simpleSuffix = "_simple.json"

#filter_obj = dict(filter_key="Server", filter_value="cache-03")

plt_styles = ['k--', 'b-.', 'r:', 'm-', 'y-', 'g-']
line_styles = ['-', '--', ':', '-']

## Get all dash client QoE files
dash_client_files = glob.glob(dataFolder + "*" + simpleSuffix)
print dash_client_files

## Filter client names by their locations
client_filter = '0824'

## Draw all chunk QoEs versus the timestampes
clientNum = 0
clientNames = []
legend_list = []
filtered_clients = []
fig, ax = plt.subplots()
minTS = None
maxTS = None
for client_file in dash_client_files:
	## Parse DASH Results
	client = re.search(dataFolder + "(.*?)" + simpleSuffix, client_file).group(1)
	print "Processing file for client, ", client
	if client_filter in client:
		dashDat = json.load(open(client_file))
		# if get_filtered_vals(dashDat, filter_obj):
		filtered_clients.append(client)

		client_name = client.split('_')[0]

		if client_name not in clientNames:
			clientNames.append(client_name)
			clientNum = clientNum + 1

		clientID = clientNames.index(client_name)
		
		ts, rsptimes = getChunkRspTime(dashDat)
		plt.plot(ts, rsptimes, plt_styles[clientID], label=client_name if client_name not in legend_list else None, linestyle=line_styles[clientID], linewidth=2.0, markersize=8)
		legend_list.append(client_name)
		print ts
		print rsptimes
		
		if minTS is None:
			minTS = min(ts)
		else:
			minTS = min(minTS, min(ts))
		if maxTS is None:
			maxTS = max(ts)
		else:
			maxTS = max(maxTS, max(ts))

print minTS, maxTS

## Change the time stamp ticks
num_intvs = int((maxTS - minTS)/300) + 1
ts_labels = [minTS + x*300 for x in range(num_intvs)]
str_ts = [datetime.datetime.fromtimestamp(x*300 + minTS).strftime('%H:%M') for x in range(num_intvs)]
plt.xticks(ts_labels, str_ts, fontsize=15)

ax.set_xlabel("Time", fontsize=20)
ax.set_ylabel("Chunk Response Time(secondes)", fontsize=20)

ax.legend(loc='upper right')

# plt.ylim((0,6))
plt.xlim((minTS, maxTS))
plt.show()

pdf = PdfPages(dataFolder + 'imgs/byzantine_type2_clients_rsptime.pdf')
pdf.savefig(fig)

pdf.close()