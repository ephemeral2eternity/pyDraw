## The overlay construction simulation script
import random
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from rstPlots.save_fig import *

def construct_overlay(N):
    nodes = range(N)

    nodes_tobe_connected = nodes

    node_degrees = {}

    while nodes_tobe_connected:
        node = nodes_tobe_connected.pop(random.randint(0,len(nodes_tobe_connected)-1))
        if not node_degrees:
            node_degrees[node] = 0
        else:
            connect_to = random.choice(node_degrees.keys())
            node_degrees[connect_to] += 1
            node_degrees[node] = 1

    max_degree = max(node_degrees.values())

    return max_degree

def test_run(node_nums):
    max_degrees = []
    for num in node_nums:
        print "Constructing overlay network for ", num, " nodes."
        cur_time = time.time()
        max_degree =  construct_overlay(num)
        time_elapsed = time.time() - cur_time
        print "Time processing ", num, "nodes is:", str(time_elapsed), " seconds!"
        max_degrees.append(max_degree)
        print "The maximum degree fot the overlay is: ", max_degree
    return max_degrees


if __name__ == "__main__":
    plt_styles = ['k-', 'b--', 'r-.', 'm-', 'y-', 'g-']
    node_nums = [10, 100, 1000, 10000, 100000, 100000, 1000000]
    imgFolder = 'D://GitHub/pyDraw/tcc-imgs/'
    max_degrees1 = test_run(node_nums)
    max_degrees2 = test_run(node_nums)
    max_degrees3 = test_run(node_nums)

    fig, ax = plt.subplots()
    plt.plot(node_nums, max_degrees1, plt_styles[0], label="Run 1")
    plt.plot(node_nums, max_degrees2, plt_styles[1], label="Run 2")
    plt.plot(node_nums, max_degrees3, plt_styles[2], label="Run 3")
    plt.xlabel("The number of nodes", fontsize=20)
    plt.ylabel("The maximum node degree", fontsize=20)
    plt.xscale('log')
    plt.yscale('log')
    plt.legend(loc=4)


    save_fig(fig, imgFolder+"max-degrees-million", fmt=".all")
    plt.show()
    plt.close(fig)
