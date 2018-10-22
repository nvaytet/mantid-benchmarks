import matplotlib.pyplot as plt
import numpy as np

data = np.loadtxt('cpu_activity_001thread.txt')

fin = open('algotimeregister.out','r')
alg_name = []
alg_start = []
alg_end = []
for line in fin.readlines():
    sl = line.split(':')
    alg_name.append(sl[0].split(">")[2])
    alg_start.append(float(sl[1].split("<")[0])/1000.0)
    alg_end.append(float(sl[1].split(">")[1])/1000.0)









fig = plt.figure()
ratio = 0.3
sizex = 30.0
fig.set_size_inches(sizex,ratio*sizex)
ax1 = fig.add_subplot(111)
# ax2 = fig.add_subplot(212)
ax2 = ax1.twinx()

ax1.plot(data[:,0],data[:,1], color='b')
ax2.plot(data[:,0],data[:,2]/1000.0, color='r')

y1 = 100.0
y2 = -500.0
y3 = -700.0
step = 200.0
colors = ['k','cyan']
k = -1
for i in range(len(alg_name)):
    if alg_end[i] - alg_start[i] > 1:
        k += 1
        ax1.plot([alg_start[i],alg_start[i]],[y1-k*step,y2-k*step], clip_on=False,color=colors[i%2],lw=1)
        ax1.plot([alg_end[i],alg_end[i]],[y1-k*step,y2-k*step], clip_on=False,color=colors[i%2],lw=1)
        ax1.plot([alg_start[i],alg_end[i]],[y2-k*step,y2-k*step], clip_on=False,color=colors[i%2],lw=1)
        ax1.plot([0.5*(alg_start[i]+alg_end[i]),0.5*(alg_start[i]+alg_end[i])],[y2-k*step,y3-k*step], clip_on=False,color=colors[i%2],lw=1)
        ax1.text(0.5*(alg_start[i]+alg_end[i]),y3-k*step, alg_name[i],rotation=90.0,ha='center',va='top',color=colors[i%2])

ax1.set_xlabel("Time (s)")
ax1.set_ylabel("CPU (%)", color='b')
ax2.set_ylabel("Memory (GB)", color='r')
ax1.set_ylim([-100.0,2500.0])

fig.savefig("cpu_memory_usage.pdf", bbox_inches="tight")
