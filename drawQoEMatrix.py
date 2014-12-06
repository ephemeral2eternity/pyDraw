from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import json
from matplotlib.backends.backend_pdf import PdfPages

qoeMat = json.load(open("./data/QoEMatrix.json"))

agentHatches = ['*', '/', '.', '\\', '+', 'x']
cacheAgents = ['agens-01', 'agens-02', 'agens-04', 'agens-05', 'agens-08', 'agens-09']
allServers = ['agens-01', 'agens-02', 'agens-03', 'agens-04', 'agens-05', 'agens-06', 'agens-07', 'agens-08', 'agens-09']
xtickName = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9']
ytickName = ['A1', 'A2', 'A4', 'A5', 'A8', 'A9']
cacheAgentsPos = [1,2,4,5,8,9]
allServersPosition = [1, 2, 3, 4, 5, 6, 7, 8, 9]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for c, z, agent, h in zip(['r', 'y', 'b', 'm', 'g', 'c'], cacheAgentsPos, cacheAgents, agentHatches):
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
