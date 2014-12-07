from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import json
from matplotlib.backends.backend_pdf import PdfPages

qoeMat = json.load(open("./data/QoEMatrix.json"))

agentHatches = ['*', '/', '.', '\\', 'o', '+', 'x', '0']
cacheAgents = ['cache-agent-01', 'cache-agent-02', 'cache-agent-03', 'cache-agent-04', 'cache-agent-05', 'cache-agent-06', 'cache-agent-07', 'cache-agent-08']
allServers = ['cache-agent-01', 'cache-agent-02', 'cache-agent-03', 'cache-agent-04', 'cache-agent-05', 'cache-agent-06', 'cache-agent-07', 'cache-agent-08']
xtickName = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8']
ytickName = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8']
cacheAgentsPos = [1,3,5,7,9,11,13,15]
allServersPosition = [1, 3, 5, 7, 9, 11, 13, 15]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for c, z, agent, h in zip(['r', 'y', 'b', 'm', 'g', 'c', '#eeefff', '#a2a7ff'], cacheAgentsPos, cacheAgents, agentHatches):
    xs = allServersPosition
    ys = []
    qoeVec = qoeMat[agent]
    for s in allServers:
    	ys.append(qoeVec[s])

    # You can provide either a single color or an array. To demonstrate this,
    # the first bar of each set will be colored cyan.
    cs = [c] * len(xs)
    cs[0] = 'c'
    ax.bar(xs, ys, zs=z, zdir='y', color=c, alpha=0.75, hatch=h)

ax.set_xlabel('Servers to be evaluated')
ax.set_ylabel('Cache Agents')
ax.set_zlabel('QoE Evaluaiton')

plt.xticks(allServersPosition, xtickName)
plt.yticks(cacheAgentsPos, ytickName)

plt.show()

pdf = PdfPages('./imgs/qoeMatrix.pdf')
pdf.savefig(fig)

pdf.close()
