import matplotlib.pyplot as plt
import numpy as np
import sys

from timestamp_tree import *
from generic_tree import Node

basename = sys.argv[1] + "_"
nthreads_list = [1,2,4,8,12,16,20,24]

tot_time = dict()
raw_time = dict()

for i in nthreads_list:
    # print(i)
    # Read in algorithm timing log and build tree
    header, records = fromFile(basename+str(i)+".out")
    # records = [x for x in records if x["finish"] - x["start"] > 100000000]
    tree = toTrees(records)[-1]
    # Compute raw durations
    raw_tree = tree.apply(lambda x: [x[0], x[2] - x[1]])
    raw_tree = raw_tree.apply_from_head_childs(lambda x, y: [x[0], x[1] - sum([a[1] for a in y])])
    header = int(header.split(':')[1])
    for node in tree.to_list():
        key = node.info[0]
        if key in tot_time.keys():
            tot_time[key].append((node.info[2]-node.info[1])/1.0e+09)
            # raw_time[key].append(float(arr[3]))
        else:
            tot_time[key] = [(node.info[2]-node.info[1])/1.0e+09]
            # raw_time[key] = [float(arr[3])]
    for node in raw_tree.to_list():
        key = node.info[0]
        if key in raw_time.keys():
            raw_time[key].append(node.info[1]/1.0e+09)
        else:
            raw_time[key] = [node.info[1]/1.0e+09]


fig = plt.figure()
ratio = 1.4
sizex = 10.0
fig.set_size_inches(sizex,ratio*sizex)
# ax1 = fig.add_subplot(111)
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)

for key in tot_time.keys():
    # print(key, tot_time[key])
    if tot_time[key][0] > 1.0 :
        # ax1.semilogy(nthreads_list,tot_time[key],'-o', label=key)
        ax1.plot(nthreads_list,tot_time[key],'-o', label=key)
    # ax2.semilogy(nthreads_list,raw_time[key],'-o', label=key)
for key in raw_time.keys():
    # print(key, raw_time[key])
    if raw_time[key][0] > 1.0 :
        # ax1.semilogy(nthreads_list,tot_time[key],'-o', label=key)
        ax2.plot(nthreads_list,raw_time[key],'-o', label=key)

ax1.set_xlabel("Number of threads")
ax1.set_ylabel("Algorithm total time")
ax1.legend(loc=(1.02,0.0),ncol=1)

ax2.set_xlabel("Number of threads")
ax2.set_ylabel("Algorithm raw time")
ax2.legend(loc=(1.02,0.0),ncol=1)

# fig.savefig("SANSReduction_timings.png", bbox_inches="tight")
fig.savefig(basename + "scaling.pdf", bbox_inches="tight")
