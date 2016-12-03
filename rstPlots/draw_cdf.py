import numpy as np
import bisect
import pylab
import sys
#from scipy.interpolate import UnivariateSpline
import matplotlib.pyplot as plt

def draw_cdf(ax, data, lineSty, legend, percentile):
	sorted_data = np.sort(data)
	yvals = np.arange(len(sorted_data))/float(len(sorted_data))
	ax.plot(sorted_data, yvals, lineSty, label=legend, linewidth=2.0)

	percentile_ind = bisect.bisect_right(yvals, 1 - percentile)
	percentile_qoe = sorted_data[percentile_ind]
	return percentile_qoe


'''
def draw_pdf(ax, data, n, ls, lg):
	p, x = np.histogram(data, bins=n)
	x = x[:-1] + (x[1] - x[0])/2
	f = UnivariateSpline(x, p, s=n)
	ax.plot(x, f(x), ls, label=lg, linewidth=2.0)
'''