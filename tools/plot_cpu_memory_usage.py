import matplotlib.pyplot as plt
import matplotlib.colors as mpc
import matplotlib.cm as mpm
from matplotlib.patches import Rectangle

import numpy as np
import sys
import copy

from timestamp_tree import *


def parse_cpu_log(filename):
    rows = []
    dct1 = {}
    dct2 = {}
    start_time = 0.0
    with open(filename, "r") as f:
        for line in f:
            if "#" in line:
                continue
            if "START_TIME:" in line:
                start_time = float(line.split()[1])
                continue
            line = line.replace("[","")
            line = line.replace("]", "")
            line = line.replace("(", "")
            line = line.replace(")", "")
            line = line.replace(",", "")
            line = line.replace("pthread", "")
            line = line.replace("id=", "")
            line = line.replace("user_time=", "")
            line = line.replace("system_time=", "")
            row = []
            lst = line.split()
            for i in range(4):
                row.append(float(lst[i]))
            i = 4
            dct1 = copy.deepcopy(dct2)
            dct2.clear()
            while i < len(lst):
                idx = int(lst[i])
                i += 1
                ut = float(lst[i])
                i += 1
                st = float(lst[i])
                i += 1
                dct2.update({idx: [ut, st]})
            count = 0
            for key, val in dct2.items():
                if key not in dct1.keys():
                    count += 1
                    continue
                elem = dct1[key]
                if val[0] != elem[0] or val[1] != elem[1]:
                    count += 1
            row.append(count)
            row.append(len(dct2))
            rows.append(row)
    return start_time, np.array(rows)


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


def smooth(y, width=1):
    box = np.ones(width)/float(width)
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth


# Read in algorithm timing log and build tree
header, records = fromFile(sys.argv[2])
records = [x for x in records if x["finish"] - x["start"] > 1.0e8]
header = int(header.split(':')[1])
# Find maximum level in all trees
lmax = 0
for tree in toTrees(records):
    for node in tree.to_list():
        lmax = max(node.level,lmax)

# Read in CPU and memory activity log
sync_time, data = parse_cpu_log(sys.argv[1])
# Number of threads allocated to this run
nthreads = int((sys.argv[1].split('_')[-1]).split('.')[0])

# Set up figure
fig = plt.figure()
ratio = 0.15
sizex = 60.0
fig.set_size_inches(sizex,ratio*sizex)
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()

x = data[:,0]-sync_time

# Plot cpu and memory usage
font_size = 30
ax1.add_patch(Rectangle((0.0, 0.0), x[-1], nthreads*100.0, edgecolor='none', facecolor='lightgrey'))
ax1.plot(x, smooth(data[:,1]), color='k', label="CPU usage")
ax2.plot(x, data[:,2]/1000.0, color='magenta', label="memory")
ax1.plot(x, smooth(data[:,4]*100.0), color='cyan', label="'active' threads usage")

# Integrate under the curve and print CPU usage fill factor
area_under_curve = np.trapz(data[:, 1], x=x)
fill_factor = area_under_curve / ((x[-1] - x[0]) * nthreads)
leg_cpu = ax1.legend(loc='lower left', bbox_to_anchor=(0.05, 0.7), frameon=False, fontsize=font_size)
leg_cpu.set_title(title="Fill factor = %.1f%%" % fill_factor, prop = {'size' : font_size})
ax2.legend(loc='lower left', bbox_to_anchor=(0.05, 0.6), frameon=False, fontsize=font_size)

# Load colormap
cm = plt.get_cmap('brg')
cNorm = mpc.Normalize(vmin=0,vmax=lmax)
scalarMap = mpm.ScalarMappable(norm=cNorm,cmap=cm)

# Plot algorithm timings
for tree in toTrees(records):
    for node in tree.to_list():
        plot_tree_node(ax1, node, lmax, sync_time, header, scalarMap)

# Finish off and save figure
ax1.set_xlabel("Time (s)", fontsize=font_size)
ax1.set_ylabel("CPU (%)", color='k', fontsize=font_size)
ax2.set_ylabel("Memory (GB)", color='magenta', fontsize=font_size)
ax1.set_ylim([-100.0, 2500.0])
ax1.grid(color='grey', linestyle='dotted')
fig.savefig(sys.argv[3], bbox_inches="tight")
