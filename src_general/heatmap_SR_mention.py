
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import pandas as pd
from urllib2 import urlopen 
import math
import numpy as np

S1_edges_present =  np.matrix(
[
[27279,	13213,	6930,	2205,	595],
[11760,	6360,	3510,	1231,	371],
[7313,	4117,	2341,	857,	271],
[5281,	3029,	1751,	642,	210],
[4007,	2320,	1346,	508,	173],
[2368,	1396,	853,	341,	135],
[1076,	660,	413,	166,	71],
[275,	182,	123,	51,	22]
]
)

S2_pct_edges = np.matrix(
[
[0.2730357322,	0.1322490241,	0.0693624262,	0.0220698629,	0.0059553598],
[0.3514014223,	0.1900436264,	0.1048825674,	0.0367836013,	0.0110858782],
[0.3817204301,	0.2148971709,	0.1221943835,	0.0447332707,	0.0141455267],
[0.4064183469,	0.2331075881,	0.1347545021,	0.0494074188,	0.0161613052],
[0.4253715499,	0.2462845011,	0.1428874735,	0.0539278132,	0.0183651805],
[0.465043205,	0.2741555381,	0.1675176748,	0.0669677926,	0.026512176],
[0.544534413,	0.3340080972,	0.2090080972,	0.0840080972,	0.0359311741],
[0.6070640177,	0.4017660044,	0.2715231788,	0.1125827815,	0.0485651214],
]
)

S = np.matrix(
[
[2.94,	2.91,	3.01,	3.67,	5.26],
[3.78,	4.18,	4.55,	6.12,	9.79],
[4.11,	4.72,	5.30,	7.45,	12.49],
[4.37,	5.12,	5.85,	8.23,	14.27],
[4.57,	5.41,	6.20,	8.98,	16.22],
[5.00,	6.03,	7.27,	11.15,	23.42],
[5.86,	7.34,	9.07,	13.99,	31.74],
[6.53,	8.83,	11.79,	18.75,	42.89],
]
)


# Normalize data columns
#S = (nba - nba.mean()) / (nba.max() - nba.min())
# Plot it out
fig, ax = plt.subplots()
#heatmap = ax.pcolor(np.array(S), cmap=plt.cm.Greens, alpha=0.99)
heatmap = ax.pcolor(np.array(S), cmap=plt.cm.Greens, norm=colors.LogNorm(vmin=S.min(), vmax=S.max()))

print S.min(), S.max()

##################################################
## FORMAT ##
##################################################
fig = plt.gcf()
fig.set_size_inches(8,11)

# turn off the frame
ax.set_frame_on(False)

# put the major ticks at the middle of each cell
ax.set_yticks(np.arange(S.shape[0])+0.5, minor=False)
ax.set_xticks(np.arange(S.shape[1])+0.5, minor=False)

# want a more natural, table-like display
#ax.invert_yaxis()
ax.xaxis.tick_top()

ax.yaxis.tick_right()

# Set the labels
xlabels = [str(x) for x in  [0.2, 0.4, 0.6, 0.8, 0.9]]
ylabels = [str(x) for x in  [1,5,10,15,20,30,50,100]]

# note I could have used nba_sort.columns but made "labels" instead
ax.set_xticklabels(xlabels, minor=False) 
ax.set_yticklabels(ylabels, minor=False)


# rotate the 
plt.xticks(rotation=90)

ax.grid(False)

plt.xlabel('SR threshold')
plt.ylabel('# of mentions')

# Turn off all the ticks
ax = plt.gca()

for t in ax.xaxis.get_major_ticks(): 
    t.tick1On = False 
    t.tick2On = False 
for t in ax.yaxis.get_major_ticks(): 
    t.tick1On = False 
    t.tick2On = False  

#vbar = fig.colorbar(heatmap, ax=ax, extend='max', ticks=[0, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
#vbar.ax.set_yticklabels([str(x) for x in [0, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]])

#plt.show()
plt.savefig("/home/sscepano/Projects7s/Twitter-workspace/DATA/General/SR_on_MENT/edges_vs_random.png", dpi=700)