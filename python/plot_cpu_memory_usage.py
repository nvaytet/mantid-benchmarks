import matplotlib.pyplot as plt
import matplotlib.colors as mpc
import matplotlib.cm as mpm

import numpy as np
import sys

from timestamp_tree import *
from generic_tree import Node


def plot_tree_node(ax, node, lmax, sync_time, header, scalarMap):

    colorVal = scalarMap.to_rgba(node.level)
    y1 = 100.0
    size = 200.0
    spacing = 700.0

    y2 = y1 - (lmax-node.level+1)*spacing
    y3 = y2 - size

    x1 = ((node.info[1] + header) / 1.0e9) - sync_time
    x2 = ((node.info[2] + header) / 1.0e9) - sync_time
    x3 = 0.5 * (x1 + x2)

    ax.plot([x1, x1, x3, x2, x2], [y1, y2, y3, y2, y1], clip_on=False, color=colorVal, lw=1)
    ax.text(x3, y3, node.info[0], rotation=90.0, ha='center', va='top', color=colorVal)


# Read in algorithm timing log and build tree
header, records = fromFile(sys.argv[2])
records = [x for x in records if x["finish"] - x["start"] > 1.0e8]
header = int(header.split(':')[1])
# Find maximum level in all trees
for tree in toTrees(records):
    lmax = 0
    for node in tree.to_list():
        lmax = max(node.level,lmax)

# Read in CPU and memory activity log
data = np.loadtxt(sys.argv[1])
# This is the synchronization time
sync_time = data[0,0]

# Set up figure
fig = plt.figure()
ratio = 0.15
sizex = 60.0
fig.set_size_inches(sizex,ratio*sizex)
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()

# Plot cpu and memory usage
ax1.plot(data[:,0]-sync_time,data[:,1], color='k')
ax2.plot(data[:,0]-sync_time,data[:,2]/1000.0, color='magenta')

# Load colormap
cm = plt.get_cmap('brg')
cNorm = mpc.Normalize(vmin=0,vmax=lmax)
scalarMap = mpm.ScalarMappable(norm=cNorm,cmap=cm)

# Plot algorithm timings
for tree in toTrees(records):
    for node in tree.to_list():
        plot_tree_node(ax1,node,lmax,sync_time,header,scalarMap)

# Finish off and save figure
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("CPU (%)", color='k')
ax2.set_ylabel("Memory (GB)", color='magenta')
ax1.set_ylim([-100.0,2500.0])
ax1.grid(color='lightgrey', linestyle='dotted')
fig.savefig(sys.argv[3], bbox_inches="tight")
