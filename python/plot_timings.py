import matplotlib.pyplot as plt
import numpy as np

# basename = "SANSReduction_nthreads_"
basename = "SNSPowderReduction_nthreads_"


nthreads_list = [1,2,4,8,12,16,20,24]
# nthreads_list = [1,2,4,8,12,16]


tot_time = dict()
raw_time = dict()

for i in nthreads_list:
    print('reading file'+basename+"%03d"%(i))
    fin = open(basename+"%03d"%(i), 'r')
    lcount = 0
    for line in fin.readlines():
        arr = line.split()
        key = arr[0]+str(lcount)+"_"+arr[1]
        if key in tot_time.keys():
            tot_time[key].append(float(arr[2]))
            raw_time[key].append(float(arr[3]))
        else:
            tot_time[key] = [float(arr[2])]
            raw_time[key] = [float(arr[3])]
        lcount += 1
    fin.close()


fig = plt.figure()
ratio = 1.4
sizex = 10.0
fig.set_size_inches(sizex,ratio*sizex)
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)

# print(tot_time)
# print(nthreads_list)

for key in tot_time.keys():
    # print(nthreads_list)
    # print(tot_time[key])
    # ax1.plot(nthreads_list,tot_time[key],'-o',label=key)
    # ax2.plot(nthreads_list,raw_time[key],'-o',label=key)
    ax1.semilogy(nthreads_list,tot_time[key],'-o', label=key)
    ax2.semilogy(nthreads_list,raw_time[key],'-o', label=key)

ax1.set_xlabel("Number of threads")
ax1.set_ylabel("Algorithm total time")
ax1.legend(loc=(0.0,1.05),ncol=3)

ax2.set_xlabel("Number of threads")
ax2.set_ylabel("Algorithm raw time")
# ax2.legend()

# fig.savefig("SANSReduction_timings.png", bbox_inches="tight")
fig.savefig("SNSPowderReduction_timings.png", bbox_inches="tight")
