import matplotlib.pyplot as plt
import matplotlib.colors as mpc
import matplotlib.cm as mpm
from matplotlib.patches import Rectangle

import numpy as np
import sys
import copy

from timestamp_tree import *
import random


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


def stringToColor(string):

    RGBint = hash(string)
    blu =  RGBint & 255
    grn = (RGBint >> 8) & 255
    red = (RGBint >> 16) & 255
    return "rgb(%i,%i,%i)" % (red,grn,blu)



def treeNodeToHtml(node, lmax, sync_time, header, count, tot_time):

    x0 = ((node.info[1] + header) / 1.0e9) - sync_time
    x1 = ((node.info[2] + header) / 1.0e9) - sync_time
    x2 = 0.5 * (x0 + x1)
    y0 = 0.0
    y1 = -(lmax-node.level+1)
    dt = x1 - x0

    # Get unique color from algorithm name
    color = stringToColor(node.info[0].split(' ')[0])
    # Compute raw time and percentages
    rawTime = dt
    if len(node.children) > 0:
        for ch in node.children:
            rawTime -= (ch.info[2] - ch.info[1]) / 1.0e9
    percTot = dt * 100.0 / tot_time
    percRaw = rawTime * 100.0 / tot_time

    boxText = node.info[0] + " : "
    if dt < 0.1:
        boxText += "%.1E" % dt
    else:
        boxText += "%.1f" % dt
    boxText += "s (%.1f%%) | %.1fs (%.1f%%)<br>" % (percTot,rawTime,percRaw)

    if node.parent is not None:
        boxText += "Parent: " + node.parent.info[0] + "<br>"
    if len(node.children) > 0:
        boxText += "Children: <br>"
        for ch in node.children:
            boxText += "  - " + ch.info[0] + "<br>"

    outputString = "trace%i = {\n" % count
    outputString += "x: [%f, %f, %f, %f, %f],\n" % (x0, x0, x2, x1, x1)
    outputString += "y: [%f, %f, %f, %f, %f],\n" % (y0, y1, y1, y1, y0)
    outputString += "fill: 'tozeroy',\n"
    outputString += "fillcolor: '" + color + "',\n"
    outputString += "line: {\n"
    outputString += "color: '#000000',\n"
    outputString += "dash: 'solid',\n"
    outputString += "shape: 'linear',\n"
    outputString += "width: 1.0\n"
    outputString += "},\n"
    outputString += "mode: 'lines+text',\n"
    outputString += "text: ['', '', '%s', '', ''],\n" % node.info[0]
    outputString += "textposition: 'top',\n"
    outputString += "textfont: {\n"
    outputString += "  color: '#ffffff',\n"
    outputString += "},\n"
    outputString += "hovertext: '" + boxText + "',\n"
    outputString += "hoverinfo: 'text',\n"
    outputString += "type: 'scatter',\n"
    outputString += "xaxis: 'x',\n"
    outputString += "yaxis: 'y3',\n"
    outputString += "showlegend: false,\n"
    outputString += "};\n"

    return outputString


def smooth(y, width=1):
    box = np.ones(width)/float(width)
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth


file_basename = sys.argv[1]

# Read in algorithm timing log and build tree
header, records = fromFile(file_basename+".out")
records = [x for x in records if x["finish"] - x["start"] > 1.0e8]
header = int(header.split(':')[1])
# Find maximum level in all trees
lmax = 0
for tree in toTrees(records):
    for node in tree.to_list():
        lmax = max(node.level,lmax)

# Read in CPU and memory activity log
sync_time, data = parse_cpu_log(file_basename+".cpu")
# Number of threads allocated to this run
nthreads = int(((file_basename)).split('_')[-1])

# Set up figure
fig = plt.figure()
ratio = 0.15
sizex = 60.0
fig.set_size_inches(sizex,ratio*sizex)
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()

x = data[:,0]-sync_time

# Plot cpu and memory usage

rect = ax1.add_patch(Rectangle((0.0,0.0),x[-1],nthreads*100.0,edgecolor='none',facecolor='lightgrey')) #,label="Maximum CPU load")
line1 = ax1.plot(x, smooth(data[:,1]), color='k', label="CPU")
line2 = ax2.plot(x, data[:,2]/1000.0, color='magenta', label="RAM")
line3 = ax1.plot(x, smooth(data[:,4]*100.0), color='cyan', label="Number of active threads")
# line4 = ax1.plot(x, data[:,5]*100.0, color='green', label="Threads created (active or waiting)")

# added these three lines
lines = line1 + line2 + line3# + line4
labs = [l.get_label() for l in lines]

# Integrate under the curve and print CPU usage fill factor
area_under_curve = np.trapz(data[:, 1], x=x)
fill_factor = area_under_curve / ((x[-1] - x[0]) * nthreads)
font_size = 30
ax1.text(0,2400.0,"Fill factor = %.1f%%" % fill_factor,ha='left',va='top',fontsize=font_size)

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
ax1.legend(lines, labs, loc=(0.3,1.05), ncol=4, fontsize=font_size)
fig.savefig(file_basename+".pdf", bbox_inches="tight")


# Create HTML output with Plotly ###############################################

htmlFname = file_basename+".html"
htmlFile = open(htmlFname,'w')
htmlFile.write("<head>\n")
htmlFile.write("  <script src=\"https://cdn.plot.ly/plotly-latest.min.js\"></script>\n")
htmlFile.write("</head>\n")
htmlFile.write("<body>\n")
htmlFile.write("  <div id=\"myDiv\"></div>\n")
htmlFile.write("  <script>\n")
# CPU
htmlFile.write("  var trace1 = {\n")
htmlFile.write("    'x': [\n")
for i in range(len(x)):
    htmlFile.write("%f,\n" % x[i])
htmlFile.write("],\n")
htmlFile.write("    'y': [\n")
for i in range(len(x)):
    htmlFile.write("%f,\n" % data[i,1])
htmlFile.write("],\n")
htmlFile.write("  'xaxis': 'x',\n")
htmlFile.write("  'yaxis': 'y1',\n")
htmlFile.write("  type: 'scatter',\n")
htmlFile.write("  name:'CPU',\n")
htmlFile.write("};\n")
# RAM
htmlFile.write("  var trace2 = {\n")
htmlFile.write("    x: [\n")
for i in range(len(x)):
    htmlFile.write("%f,\n" % x[i])
htmlFile.write("],\n")
htmlFile.write("    y: [\n")
for i in range(len(x)):
    htmlFile.write("%f,\n" % (data[i,2]/1000.0))
htmlFile.write("],\n")
htmlFile.write("  xaxis: 'x',\n")
htmlFile.write("  yaxis: 'y2',\n")
htmlFile.write("  type: 'scatter',\n")
htmlFile.write("  name:'RAM',\n")
htmlFile.write("};\n")
# Active threads
htmlFile.write("  var trace3 = {\n")
htmlFile.write("    x: [\n")
for i in range(len(x)):
    htmlFile.write("%f,\n" % x[i])
htmlFile.write("],\n")
htmlFile.write("    y: [\n")
for i in range(len(x)):
    htmlFile.write("%f,\n" % (data[i,4]*100.0))
htmlFile.write("],\n")
htmlFile.write("  xaxis: 'x',\n")
htmlFile.write("  yaxis: 'y1',\n")
htmlFile.write("  type: 'scatter',\n")
htmlFile.write("  name:'Active threads',\n")
htmlFile.write("};\n")

count = 4
dataString = "[trace1,trace2,trace3"
for tree in toTrees(records):
    for node in tree.to_list():
        htmlFile.write(treeNodeToHtml(node, lmax, sync_time, header, count, x[-1]))
        dataString += ",trace%i" % count
        count += 1
dataString += "]"

htmlFile.write("var data = " + dataString + ";\n")
htmlFile.write("var layout = {\n")
htmlFile.write("  'height': 700,\n")
htmlFile.write("  'xaxis' : {\n")
htmlFile.write("    'domain' : [0, 1.0],\n")
htmlFile.write("    'title' : 'Time (s)',\n")
htmlFile.write("    'side' : 'top',\n")
htmlFile.write("  },\n")
htmlFile.write("  'yaxis1': {\n")
htmlFile.write("    'domain' : [0.5, 1.0],\n")
htmlFile.write("    'title': 'CPU (%)',\n")
htmlFile.write("    'side': 'left',\n")
htmlFile.write("    'fixedrange': true,\n")
htmlFile.write("    },\n")
htmlFile.write("  'yaxis2': {\n")
htmlFile.write("    'title': 'RAM (GB)',\n")
htmlFile.write("    'overlaying': 'y1',\n")
htmlFile.write("    'side': 'right',\n")
htmlFile.write("    'fixedrange': true,\n")
htmlFile.write("    'showgrid': false,\n")
htmlFile.write("    },\n")
htmlFile.write("  'yaxis3': {\n")
htmlFile.write("    'domain' : [0, 0.5],\n")
htmlFile.write("    'anchor' : 'x',\n")
htmlFile.write("    'showgrid': false,\n")
htmlFile.write("    'ticks': '',\n")
htmlFile.write("    'showticklabels': false,\n")
htmlFile.write("    'fixedrange': true,\n")
htmlFile.write("    'side': 'left',\n")
htmlFile.write("    },\n")
htmlFile.write("  'hovermode' : 'closest',\n")
htmlFile.write("  'hoverdistance' : 100,\n")
htmlFile.write("  'legend': {\n")
htmlFile.write("    'x' : 0,\n")
htmlFile.write("    'y' : 1.1,\n")
htmlFile.write("    'orientation' : 'h',\n")
htmlFile.write("  },\n")
htmlFile.write("  'annotations': [{\n")
htmlFile.write("    xref: 'paper',\n")
htmlFile.write("    yref: 'paper',\n")
htmlFile.write("    x: 1,\n")
htmlFile.write("    xanchor: 'right',\n")
htmlFile.write("    y: 1.1,\n")
htmlFile.write("    yanchor: 'bottom',\n")
htmlFile.write("    text: 'Fill factor: %.1f%%',\n" % fill_factor)
htmlFile.write("    showarrow: false\n")
htmlFile.write("  }],\n")
htmlFile.write("  'shapes': [{\n")
htmlFile.write("      layer: 'below',\n")
htmlFile.write("      fillcolor: '#E0E0E0',\n")
htmlFile.write("      line : {\n")
htmlFile.write("        width: 0,\n")
htmlFile.write("      },\n")
htmlFile.write("      x0: 0.0,\n")
htmlFile.write("      x1: %f,\n" % x[-1])
htmlFile.write("      y0: 0,\n")
htmlFile.write("      y1: %i,\n" % (nthreads*100))
htmlFile.write("      xref: 'x',\n")
htmlFile.write("      yref: 'y1',\n")
htmlFile.write("    }],\n")
htmlFile.write("};\n")
htmlFile.write("Plotly.newPlot('myDiv', data, layout, {scrollZoom: true});\n")
htmlFile.write("</script>\n</body>\n</html>\n")
htmlFile.close()
